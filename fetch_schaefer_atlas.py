# Fetch Schaefer parcellation

import configparser
import os
import requests
import shutil

config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']


url = (
    'https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/'
    '/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI'
    'Schaefer2018_200Parcels_7Networks_order_FSLMNI152_2mm.nii.gz'
    '?raw=true'
    )

path = os.path.join(WORK_DIR, 'schaefer200.nii.gz')

with requests.get(url, stream=True) as r:
    with open(path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)

# download the labels as well

url = (
    'https://github.com/ThomasYeoLab/CBIG/raw/master/stable_projects/'
    'brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI/'
    'Schaefer2018_200Parcels_7Networks_order.txt'
    )

path = path.replace('nii.gz', 'tsv')

with requests.get(url, stream=True) as r:
    with open(path, 'wt') as f:
        f.write(r.text)
