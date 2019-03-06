# Fetch Schaefer parcellation

import configparser
import requests
import shutil

config = configparser.ConfigParser()
config.read('movrest_config.ini')
WORK_DIR = config['DEFAULT']['WORK_DIR']


url = ''
path = ''

# https://github.com/ThomasYeoLab/CBIG/tree/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/MNI

with requests.get(url, stream=True) as r:
    with open(path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
