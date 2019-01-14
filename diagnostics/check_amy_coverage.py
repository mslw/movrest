"""
This script counts voxels overlapping between SPM's 1st level masks
and bilateral amygdala ROI taken from Harvard - Oxford atlas
"""

import argparse
from nilearn import datasets, plotting, image
import numpy as np
import configparser
from bids import BIDSLayout
import os

# config
config = configparser.ConfigParser()
config.read('movrest_config.ini')
SOURCE_DIR = config['DEFAULT']['SOURCE_DIR']
WORK_DIR = config['DEFAULT']['WORK_DIR']

# args
parser = argparse.ArgumentParser()
parser.add_argument('--plot', action='store_true',
                    help='Plot the amygdala ROI')
parser.add_argument('--save', action='store_true',
                    help='Save the amygdala ROI in WORK_DIR/masks')
args = parser.parse_args()

# fetch atlas & prepare mask
dataset = datasets.fetch_atlas_harvard_oxford('sub-maxprob-thr25-2mm')
atlas_filename = dataset.maps
labels = dataset.labels

atlas = image.load_img(atlas_filename)
atlas_data = atlas.get_data()

mask_data = np.zeros(atlas_data.shape, dtype=np.int32)
mask_data[atlas_data == labels.index('Left Amygdala')] = 1
mask_data[atlas_data == labels.index('Right Amygdala')] = 1

mask = image.new_img_like(atlas, mask_data)

if args.plot:
    plotting.plot_roi(mask)
    plotting.show()
if args.save:
    out_fname = os.path.join(WORK_DIR, 'masks', 'amy_mask.nii')
    mask.to_filename(out_fname)
    print('Saved', out_fname)

# will need to resample, but shape theoretically unknown, so start with None
res_mask = None
res_mask_data = None
vox_in_mask = None

# use pybids to grab files
layout = BIDSLayout(SOURCE_DIR)
subjects = layout.get_subjects()

# loop all subjects
msg = 'Subject {}: {} voxels overlap ({}%)'

for subject in subjects:
    mask_path = os.path.join(WORK_DIR,
                             'models',
                             'sub-{}'.format(subject),
                             'mask.nii')
    spm_mask = image.load_img(mask_path)
    spm_mask_data = spm_mask.get_data()

    if res_mask is None or res_mask.shape != spm_mask.shape:
        res_mask = image.resample_to_img(mask, spm_mask,
                                         interpolation='nearest')
        res_mask_data = res_mask.get_data()
        vox_in_mask = np.sum(res_mask_data)

    overlap = np.sum(np.logical_and(spm_mask_data, res_mask_data))
    overlap_pct = int(overlap / vox_in_mask * 100)

    print(msg.format(subject, overlap, overlap_pct))
