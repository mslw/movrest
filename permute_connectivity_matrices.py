import configparser
import glob
import numpy as np
import os

# get path to work dir
config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

# hardcoded constants
WORK_SUBDIR = 'nilearn_connectivity'
N_BOOT = 10000

# load all connectivity matrices, calculate difference relative to post-neu
all_diffs = []
for f in glob.glob(os.path.join(WORK_DIR, WORK_SUBDIR, '*.npy')):
    # todo filter subjects
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
