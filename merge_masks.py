"""
This program merges masks created by fmriprep for both runs of movierest task
by creating their overlap. Such mask can be used as an explicit mask
in first level model (this will mask out e.g. eyes, but not white matter).
"""

from bids import BIDSLayout
import configparser
import matplotlib.pyplot as plt
import numpy as np
import os
from nilearn.image import load_img, new_img_like
from nilearn.plotting import plot_roi
import warnings

# get paths to fmriprep and work directories from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')
PREP_DIR = config['DEFAULT']['PREP_DIR']
WORK_DIR = config['DEFAULT']['WORK_DIR']

layout = BIDSLayout(PREP_DIR)

# prepare subplots to plot a quick overview of masks
n_subjects = len(layout.get_subjects())
fig, axs = plt.subplots(int(np.ceil(n_subjects/3)), 3, figsize=(18, 12))
axs_flat = axs.flat

for subject_id in layout.get_subjects():

    files = layout.get(subject=subject_id, task='movierest', type='mask')

    run1 = layout.get(subject=subject_id, task='movierest', type='mask', run=1)
    run2 = layout.get(subject=subject_id, task='movierest', type='mask', run=2)

    mask1 = load_img(files[0].filename)
    mask2 = load_img(files[1].filename)

    # using [0] and [1] above, so warn if query gave more or less than 2
    if len(files) != 2:
        warnings.warn(
            'Weird number of masks found for subject {}'.format(subject_id),
            RuntimeWarning)

    mask1_data = mask1.get_data().astype(bool)
    mask2_data = mask2.get_data().astype(bool)

    overlap = np.logical_and(mask1_data, mask2_data).astype(np.uint8)
    mask = new_img_like(mask1, overlap)
    mask.to_filename(os.path.join(WORK_DIR,
                                  'masks',
                                  'sub-{}_explicitmask.nii'.format(subject_id)
                                  ))

    plot_roi(mask, title=subject_id, axes=next(axs_flat), display_mode='yx')
    plt.suptitle('fmriprep brain masks (BOLD), merged')

plt.savefig(os.path.join(WORK_DIR, 'diagnostic_plots', 'mriqc_merged_masks'))
