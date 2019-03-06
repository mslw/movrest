import argparse
import configparser
import math
import numpy as np
import os
import pandas

from nilearn.input_data import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure

from bids import BIDSLayout
from collections import defaultdict


def get_rest_regressors(filename):
    wanted = [
        'csf', 'white_matter', 'global_signal',
        'trans_x', 'trans_y', 'trans_z',
        'rot_x', 'rot_y', 'rot_z',
        'a_comp_cor_00', 'a_comp_cor_01', 'a_comp_cor_02',
        'a_comp_cor_03', 'a_comp_cor_04', 'a_comp_cor_05',
        'framewise_displacement',
        ]

    t = pandas.read_table(filename)
    regressors = t.loc[:, wanted]
    regressors.fillna(value=0, inplace=True)

    return regressors.values


def time_to_volume(time, tr):
    return math.ceil(time / tr)


def get_epochs(time_series, t_type, events_table, n_vol, t_r):
    onsets = events_table.query('trial_type==@t_type').onset
    start_volumes = [time_to_volume(t, t_r) for t in onsets]
    epochs = [time_series[s:s+n_vol, :] for s in start_volumes]
    return np.array(epochs)


# some constants
N_VOL_REST = 80  # how many resting volumes per epoch
REPETITION_TIME = 1.1
WORK_SUBDIR = 'nilearn_connectivity_schaefer'

# get input arguments
parser = argparse.ArgumentParser()
parser.add_argument('subject_id')
args = parser.parse_args()
SUBJECT_ID = args.subject_id

# get paths to fmriprep and work directories from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')
PREP_DIR = config['DEFAULT']['PREP_DIR']
SOURCE_DIR = config['DEFAULT']['SOURCE_DIR']
WORK_DIR = config['DEFAULT']['WORK_DIR']

# Fetch prepared ROIs
atlas_filename = os.path.join(WORK_DIR, 'schaefer200.nii.gz')

print('Atlas ROIs are located in nifti image at: %s' % atlas_filename)

# Locate the required files
layout_prep = BIDSLayout(PREP_DIR)
layout_raw = BIDSLayout(SOURCE_DIR)

# prepare data structure for signal epochs
epoch_dict = defaultdict(list)

for run_number in (1, 2):

    # bold, unsmoothed (not prefixed by SPM)
    files = layout_prep.get(
        subject=SUBJECT_ID,
        type='bold',
        task='movierest',
        run=run_number)
    files = [f for f in files
             if os.path.basename(f.filename).startswith('sub')]
    fmri_filename = files[0].filename

    # confounds
    confounds_files = layout_prep.get(
        subject=SUBJECT_ID,
        type='regressors',
        task='movierest',
        run=run_number)
    confounds_filename = confounds_files[0].filename

    # events
    events_files = layout_raw.get(
        subject=SUBJECT_ID,
        task='movierest',
        type='events',
        run=run_number)
    events_filename = events_files[0].filename

    # Extract signals on a parcellation
    # this is time (~5 minutes) and memory (OMG) consuming
    rest_regressors = get_rest_regressors(confounds_filename)
    masker = NiftiLabelsMasker(labels_img=atlas_filename,
                               standardize=True,
                               detrend=True,
                               high_pass=0.009,
                               low_pass=0.08,
                               t_r=REPETITION_TIME,
                               verbose=5,
                               )
    time_series = masker.fit_transform(fmri_filename,
                                       confounds=rest_regressors)

    # divide the time series into epochs
    events_df = pandas.read_table(events_filename)

    for emotion in ('erotic', 'fear', 'joy', 'neutral', 'sadness'):
        epochs = get_epochs(time_series=time_series,
                            t_type='rest_post_' + emotion,
                            events_table=events_df,
                            n_vol=N_VOL_REST,
                            t_r=REPETITION_TIME)
        epoch_dict[emotion].append(epochs)  # append, as there are 2 runs

# compute the correlation matrices
correlation_measure = ConnectivityMeasure(kind='correlation')

results = []
for emotion in ('erotic', 'fear', 'joy', 'neutral', 'sadness'):
    emo_epochs = np.concatenate(epoch_dict[emotion])  # concat runs
    correlation_matrix = correlation_measure.fit_transform(emo_epochs)
    cm_mean = correlation_matrix.mean(axis=0)  # average across trials
    np.fill_diagonal(cm_mean, 0)
    results.append(cm_mean)

correlation_results = np.array(results)  # shape: conditions (5) x ROIs x ROIs

# save the output
out_name = 'sub-{}_matrices.npy'.format(SUBJECT_ID)
out_dir = os.path.join(WORK_DIR, WORK_SUBDIR)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
np.save(file=os.path.join(WORK_DIR, WORK_SUBDIR, out_name),
        arr=correlation_results)
