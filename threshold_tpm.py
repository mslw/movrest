import configparser
import nibabel as nib
import numpy as np
import os

THRESHOLD = 30

config = configparser.ConfigParser()
config.read('movrest_config.ini')
SPM_DIR = config['DEFAULT']['SPM_DIR']

# use the TPM.nii distributed with SPM
tpm_path = os.path.join(SPM_DIR, 'tpm', 'TPM.nii')
tpm = nib.load(tpm_path)
gm = tpm.dataobj[:, :, :, 0]  # gray matter is in the first volume

gm_thr = np.zeros(gm.shape, dtype=np.uint16)
gm_thr[gm > THRESHOLD/100] = 1

mask = nib.Nifti1Image(gm_thr, tpm.affine)

nib.save(mask, 'tpm_grey_{}.nii'.format(THRESHOLD))
