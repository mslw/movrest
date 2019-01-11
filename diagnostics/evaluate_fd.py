"""
This script reads the FD from regressor file and calculates the number
of outliers for a given threshold (can be useful because MRIQC has a very
conservative threshold of 0.2)
"""

import argparse
from bids import BIDSLayout
import configparser
import numpy as np
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('threshold', type=float)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('movrest_config.ini')
PREP_DIR = config['DEFAULT']['PREP_DIR']

layout = BIDSLayout(PREP_DIR)
all_files = layout.get(task='movierest', type='regressors')

for f in all_files:

    t = pandas.read_table(f.filename)

    fd = t.framewise_displacement
    n_above = np.sum(fd > args.threshold)
    max_fd = np.max(fd)

    msg = 'sub-{}, run-{}: {} outliers, max {} mm'
    print(msg.format(f.subject, f.run, n_above, max_fd))
