'''
Convert BIDS events.tsv file to SPM's Names, Onsets, Durations .mat file
'''

from bids import BIDSLayout
import configparser
import csv
import numpy as np
import os
from scipy import io

# get paths to source and work directories from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')
SOURCE_DIR = config['DEFAULT']['SOURCE_DIR']
WORK_DIR = config['DEFAULT']['WORK_DIR']

# create subdirectory in args.work_dir if it does not exist yet
subdir = 'spm_inputs'
if not os.path.exists(os.path.join(WORK_DIR, subdir)):
    os.makedirs(os.path.join(WORK_DIR, subdir))

# list the conditions explicitly
# I could just get unique trial types
# but i want to change them a little
# (rename conditions and split rest into 3 parts)
# and force the order by hand

names = [
    'movie-erotic',
    'rest-erotic',
    'movie-fear',
    'rest-fear',
    'movie-joy',
    'rest-joy',
    'movie-neutral',
    'rest-neutral',
    'movie-sadness',
    'rest-sadness',
    'mental-content-question',
]


def rename_condition(trial_type):
    if trial_type == 'mentalContentQuestion':
        return('mental-content-question')
    else:
        return trial_type.replace('_post_', '_').replace('_', '-')


# use pybids to grab files
layout = BIDSLayout(SOURCE_DIR)
all_files = layout.get(task='movierest', type='events', extensions='tsv')

# loop through the files and generate .mat files
for f in all_files:

    onsets = [[] for i in range(len(names))]
    durations = [[] for i in range(len(names))]

    with open(f.filename) as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        next(reader, None)  # skip header
        for row in reader:
            onset = float(row[0])
            duration = float(row[1])
            condition = rename_condition(row[2])

            # enter as is
            idx = names.index(condition)
            onsets[idx].append(onset)
            durations[idx].append(duration)

    # build the output path
    out_name = os.path.basename(f.filename).replace('.tsv', '_90.mat')
    out_path = os.path.join(WORK_DIR, subdir, out_name)

    # save the .mat file
    mdict = {
        'names': np.array(names, dtype=np.object),
        'onsets': np.array(onsets, dtype=np.object),
        'durations': np.array(durations, dtype=np.object),
        }

    io.savemat(out_path, mdict)
