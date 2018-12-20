import configparser
import numpy as np
import nibabel as nib
import os

from nilearn import datasets

config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']

cortical = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm',
                                               symmetric_split=True)
subcortical = datasets.fetch_atlas_harvard_oxford('sub-maxprob-thr25-2mm',
                                                  symmetric_split=True)

cort_data = cortical.maps.get_data()
sub_data = subcortical.maps.get_data()


def get_cortical(label):
    idx = cortical.labels.index(label)
    mask = cort_data == idx
    return mask


def get_subcortical(label):
    idx = subcortical.labels.index(label)
    mask = sub_data == idx
    return mask


new_data = np.zeros_like(cort_data)
new_data[get_cortical('Left Insular Cortex')] = 1
new_data[get_cortical('Right Insular Cortex')] = 2
new_data[get_cortical('Left Cingulate Gyrus, anterior division')] = 3
new_data[get_cortical('Right Cingulate Gyrus, anterior division')] = 3
new_data[get_cortical('Left Cingulate Gyrus, posterior division')] = 4
new_data[get_cortical('Right Cingulate Gyrus, posterior division')] = 4
new_data[get_cortical('Left Angular Gyrus')] = 5
new_data[get_cortical('Right Angular Gyrus')] = 6
new_data[get_cortical('Left Precuneous Cortex')] = 7
new_data[get_cortical('Right Precuneous Cortex')] = 7
new_data[get_cortical('Left Paracingulate Gyrus')] = 8
new_data[get_cortical('Right Paracingulate Gyrus')] = 9

new_data[get_subcortical('Left Amygdala')] = 10
new_data[get_subcortical('Right Amygdala')] = 11
new_data[get_subcortical('Left Pallidum')] = 12
new_data[get_subcortical('Right Pallidum')] = 13
new_data[get_subcortical('Left Thalamus')] = 14
new_data[get_subcortical('Right Thalamus')] = 15

labels = [
    'Left Insular Cortex',
    'Right Insular Cortex',
    'Cingulate Gyrus, anterior division',
    'Cingulate Gyrus, posterior division',
    'Left Angular Gyrus',
    'Right Angular Gyrus',
    'Precuneous Cortex',
    'Left Paracingulate Gyrus',
    'Right Paracingulate Gyrus',
    'Left Amygdala',
    'Right Amygdala',
    'Left Pallidum',
    'Right Pallidum',
    'Left Thalamus',
    'Right Thalamus'
]

new_atlas = nib.nifti1.Nifti1Image(new_data, affine=cortical.maps.affine)
new_atlas.to_filename(os.path.join(WORK_DIR, 'selected_HO_rois.nii'))

with open(os.path.join(WORK_DIR, 'selected_HO_rois.txt'), 'w') as labels_file:
    labels_file.writelines([label + '\n' for label in labels])
