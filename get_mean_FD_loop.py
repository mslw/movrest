'''
Get mean framewise displacement for each subject
to be used as second level regressor
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

# create subdirectory in args.work_dir if it does not exist yet
subdir = 'spm_inputs'
if not os.path.exists(os.path.join(WORK_DIR, subdir)):
    os.makedirs(os.path.join(WORK_DIR, subdir))

# use BIDSLayout - works well with derivatives
layout = BIDSLayout(PREP_DIR)

subjects = layout.get_subjects()

fd_values = []

for sub_id in subjects:

    files = layout.get(subject=sub_id, task='movierest', type='regressors')

    fd = []
    for f in files:
        t = pandas.read_table(f.filename)
        t.fillna(value=0, inplace=True)
        fd.append(t.framewise_displacement.values)
    fd_concat = np.concatenate(fd)

    fd_mean = np.mean(fd_concat)
    print(sub_id, fd_mean.round(3))

    fd_values.append(fd_mean.round(3))

fname = os.path.join(WORK_DIR, subdir, 'mean_fd.mat')
io.savemat(fname, {'mean_fd': fd_values}, oned_as='column')

with open(os.path.join(WORK_DIR, subdir, 'mean_fd.txt'), 'wt') as f:
    f.writelines(['{}\n'.format(v) for v in fd_values])
