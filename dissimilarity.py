import configparser
import glob

import numpy as np
import os
import re
import scipy.spatial.distance as ssd

from nilearn import plotting
import matplotlib.pyplot as plt

# get path to work dir
config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

# hardcoded constants
WORK_SUBDIR = 'nilearn_connectivity_spheres'

# load all AVERAGED connectivity matrices
# will need to rewrite this part to read non-averaged and average them
all_avg = []
for f in glob.glob(os.path.join(WORK_DIR, WORK_SUBDIR, '*.npy')):
    subject_id = re.match('sub-([0-9]+)', os.path.basename(f)).group(1)
    if subject_id in ['10', '27']:
        # these subjects had outlying questionnaire scores
        continue
    if subject_id == 12:
        # this is the subject chosen for evaluation
        continue

    cm = np.load(f)  # category x ROI x ROI
    all_avg.append(cm)

sub_avgs = np.stack(all_avg, axis=0)  # subject x cat x roi x roi

# calculate the mean across subjects
grand_avg = np.mean(sub_avgs, axis=0)  # cat x ROI x ROI

# load from a given subject
#  cat x epoch x roi x roi
single_sub = np.load(os.path.join(WORK_DIR,
                                  'nilearn_connectivity_experimental',
                                  'sub-12_matrices.npy'))

# indices for lower triangle (without )
ti = np.tril_indices(grand_avg.shape[1], k=-1)

# i = 4
# for j in range(single_sub.shape[1]):
#     epoch_arr = single_sub[i, j, :, :]
#
#     # consider using pdist instead of doing pairwise by hand
#     for k in range(grand_avg.shape[0]):
#         dist = ssd.correlation(epoch_arr[ti], grand_avg[k, ti[0], ti[1]])
#         print(k, dist)
#     print('---')

# within subject variant
# i = 4
# single_sub = np.ma.array(single_sub)  # cat x epoch x roi x roi
# for j in range(single_sub.shape[1]):
#     epoch_arr = single_sub[i, j, :, :]
#
#     single_sub[i, j, :, :] = np.ma.masked
#     mean_excl = single_sub.mean(axis=1)  # cat x roi x roi
#     single_sub.mask = np.ma.nomask
#
#     for k in range(mean_excl.shape[0]):
#         dist = ssd.correlation(epoch_arr[ti], mean_excl[k, ti[0], ti[1]])
#         print(j, k, dist)
#     print('------')
