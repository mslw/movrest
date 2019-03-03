"""
Several plots to make talking about connectivity a bit easier

Idea 1:
Create actual spheres and save to a nifti file, so that they
can be viewed in mango or shown with nilearn plotting
Idea 2: plotting.plot_connectome
"""

import configparser
import glob
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import os
import re

from nilearn import plotting
from nltools.mask import create_sphere

config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

# copy-paste the seeds from prepare_connectivity_matrices.py
seeds = [
    (-2, 44, 2),  # ACC
    (-32, 52, 16),  # Frontal Pole
    (49, 47, 8),
    (-42, 13, 0),  # Frontal Operculum / Insula
    (41, 13, 4),
    (-13, 13, -10),  # Accumbens
    (12, 13, -9),
    (0, -25, 35),  # PCC / Middle Cingulate
    (-6, -71, 33),  # Precuneous Cortex
    (-45, -64, 39),  # Lateral Occipital Cortex sup. div. / IPL
    (47, -64, 39),
    (-31, 38, -9),  # Frontal Pole / Orbitofrontal Cortex
    (31, 39, -9),
    (-23, -3, -19),  # Amygdala
    (23, -3, -19)
]

# load all correlation matrices
fnames = glob.glob(os.path.join(WORK_DIR,
                                'nilearn_connectivity_spheres_filter',
                                'sub-??_matrices.npy'))
cmats = []
for f in fnames:
    subject_id = re.match('sub-([0-9]+)', os.path.basename(f)).group(1)
    if subject_id in ['10', '27']:
        continue
    cmat = np.load(f)
    cmats.append(cmat[0])  # let's take post-ero

cmat = np.stack(cmats, axis=0).mean(axis=0)

plotting.plot_matrix(cmat)
plotting.plot_connectome(cmat, seeds, title='post-ero connectivity')
# plotting.plot_connectome(cmat, seeds, edge_threshold='50%')

spheres = [create_sphere(seeds[i], radius=6) for i in range(len(seeds))]
sphere_sum = np.sum([img.dataobj for img in spheres], axis=0).astype(np.uint8)
spheres_img = nib.Nifti1Image(sphere_sum, spheres[0].affine)
spheres_img.to_filename(os.path.join(WORK_DIR, 'spherical_rois.nii'))

plotting.plot_roi(spheres_img,
                  cut_coords=[-18, -9, 0, 12, 36],
                  display_mode='z',
                  title='selected ROIs')
plt.show()
