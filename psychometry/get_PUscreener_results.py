from bids import BIDSLayout
import configparser
import numpy as np
import os
import pandas
import matplotlib.pyplot as plt

# get paths from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')

SOURCE_DIR = config['DEFAULT']['SOURCE_DIR']
RESPONSES_DIR = config['DEFAULT']['RESPONSES_DIR']

# get subjects from BIDS
layout = BIDSLayout(SOURCE_DIR)
subjects = layout.get_subjects()
subject_codes = ['MOVREST_{}'.format(s) for s in subjects]

# read table
df = pandas.read_table(os.path.join(RESPONSES_DIR, 'movrestb-export.csv'),
                       delimiter=',',
                       index_col=0,
                       )

# get
df.query('questionnaire=="pus"', inplace=True)
df['hasMri'] = df.kod.apply(lambda x: x in subject_codes)
df.query('hasMri', inplace=True)

scores = df.groupby('kod').answer.sum()

# print(scores)
# plt.figure(figsize=(2, 6))
# seaborn.swarmplot(scores, orient='v')

plt.figure()
plt.title('Pornography Use Screener')
plt.hist(scores, np.arange(-0.5, 9.5, 1), edgecolor='k')
plt.xticks(np.arange(0, 9))
plt.xlabel('Total score')
plt.ylabel('# subjects')
plt.show()
