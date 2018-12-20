'''
Select only required regressors from fmriprep's confounds and save them in
format required by SPM.
Files are written in WORK_DIR/spm_inputs.
The WORK_DIR and PREP_DIR are taken from a config file.
'''

from bids import BIDSLayout
import configparser
import numpy as np
import os
import pandas
from scipy import io

# get paths to fmriprep and work directories from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')
PREP_DIR = config['DEFAULT']['PREP_DIR']
WORK_DIR = config['DEFAULT']['WORK_DIR']

# list all required regressors
wanted = [
    'trans_x',
    'trans_y',
    'trans_z',
    'rot_x',
    'rot_y',
    'rot_z',
    'framewise_displacement',
    'a_comp_cor_00',
    'a_comp_cor_01',
    'a_comp_cor_02',
    'a_comp_cor_03',
    'a_comp_cor_04',
    'a_comp_cor_05',
    ]

# column headers for SPM - looks nicer on design matrix
renamed_headers = [s.replace('_', '-') for s in wanted]

# create subdirectory in args.work_dir if it does not exist yet
subdir = 'spm_inputs'
if not os.path.exists(os.path.join(WORK_DIR, subdir)):
    os.makedirs(os.path.join(WORK_DIR, subdir))

# use BIDSLayout - works well with derivatives
layout = BIDSLayout(PREP_DIR)
all_files = layout.get(task='movierest', type='regressors')

for f in all_files:
    # extract wanted regressors
    t = pandas.read_table(f.filename)
    regressors = t.loc[:, wanted]
    regressors.fillna(value=0, inplace=True)

    # build the output path & filename
    out_name = os.path.basename(f.filename).replace('.tsv', '.mat')
    out_name = out_name.replace('_desc-confounds', '')
    out_path = os.path.join(WORK_DIR, subdir, out_name)

    # save the .mat file
    mdict = {
        'names': np.array(renamed_headers, dtype=np.object),
        'R': regressors.values,
    }
    io.savemat(out_path, mdict)
