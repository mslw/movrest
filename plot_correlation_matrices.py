import configparser
import glob
import numpy as np
import os
import re

import scipy.spatial.distance as ssd

import matplotlib.pyplot as plt
import nilearn.plotting as nlp


def mat2vec(mat):
    # indices for lower triangle (without diagonal)
    ti = np.tril_indices(grand_avg.shape[1], k=-1)
    return mat[ti]


# get path to work dir
config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

# hardcoded constants
WORK_SUBDIR = 'nilearn_connectivity_schaefer'

# load all AVERAGED connectivity matrices
# will need to rewrite this part to read non-averaged and average them
all_avg = []
for f in glob.glob(os.path.join(WORK_DIR, WORK_SUBDIR, '*.npy')):
    subject_id = re.match('sub-([0-9]+)', os.path.basename(f)).group(1)
    if subject_id in ['10', '27']:
        # these subjects had outlying questionnaire scores
        continue

    cm = np.load(f)  # category x ROI x ROI
    all_avg.append(cm)

all_data = np.stack(all_avg, axis=0)  # subject x cat x roi x roi

grand_avg = all_data.mean(axis=0)  # cat x roi x roi

for i in range(grand_avg.shape[0]):
    fig = nlp.plot_matrix(grand_avg[i, :, :])
    cdist = ssd.correlation(mat2vec(grand_avg[i, :, :]),
                            mat2vec(grand_avg[3, :, :]))
    print(cdist)

plt.show()
