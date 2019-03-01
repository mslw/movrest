import configparser
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import re

from nilearn import plotting

# get path to work dir
config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

# hardcoded constants
WORK_SUBDIR = 'nilearn_connectivity_spheres_filter'
N_BOOT = 10000

# load all connectivity matrices, calculate difference relative to post-neu
all_diffs = []
for f in glob.glob(os.path.join(WORK_DIR, WORK_SUBDIR, '*.npy')):
    subject_id = re.match('sub-([0-9]+)', os.path.basename(f)).group(1)
    if subject_id in ['10', '27']:
        # these subjects had outlying questionnaire scores
        continue

    cm = np.load(f)  # category x ROI x ROI
    d = np.delete(cm, 3, 0) - cm[3, :, :]

    all_diffs.append(d)

# calculate the mean across subjects
the_mean = np.mean(np.stack(all_diffs, axis=0), axis=0)  # cat x ROI x ROI

n_subjects = len(all_diffs)

for cat_idx in range(4):
    cat_mats = []
    for sub_idx in range(n_subjects):
        cat_mats.append(all_diffs[sub_idx][cat_idx, :, :].copy())
        np.fill_diagonal(cat_mats[-1], np.NaN)  # fill diagonal with nan

    n_roi = cat_mats[0].shape[0]
    max_r_dist = np.empty((N_BOOT, n_roi))
    min_r_dist = np.empty((N_BOOT, n_roi))

    for i in range(N_BOOT):
        for k in range(n_subjects):
            np.random.shuffle(cat_mats[k].T)  # x.T is a view, this is legit

        perm_mean = np.nanmean(np.stack(cat_mats, axis=0), axis=0)

        max_r_dist[i] = np.amax(perm_mean, axis=1)
        min_r_dist[i] = np.amin(perm_mean, axis=1)

    print(cat_idx,
          np.percentile(min_r_dist, 2.5),
          np.percentile(max_r_dist, 97.5),
          )

# plot mean correlation matrices
for i in range(the_mean.shape[0]):
    plotting.plot_matrix(the_mean[i])

# also show an example of a single-subject matrix
plotting.plot_matrix(all_diffs[-1][0])
plt.show()
