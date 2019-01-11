"""
This file contains all commands needed to go from raw to clean movie rating
data. This includes removal of participants not included in the dataset (who
did not complete the scanning, so did not watch all the videos) and fixing
of the database structure to make up for incorrect insert calls.

Must be called from parent directory for config to work properly.
"""

from bids import BIDSLayout
import configparser
import os
import shutil
import sqlite3

# get paths from config file
config = configparser.ConfigParser()
config.read('movrest_config.ini')

RESPONSES_DIR = config['DEFAULT']['RESPONSES_DIR']
SOURCE_DIR = config['DEFAULT']['SOURCE_DIR']

# make a copy of raw ratings (will overwrite destination file if exists)
cleaned_path = os.path.join(RESPONSES_DIR, 'rating_results_cleaned.db')
shutil.copy(os.path.join(RESPONSES_DIR, 'rating_results.db'), cleaned_path)

conn = sqlite3.connect(cleaned_path)
c = conn.cursor()

# -- remove test rating by myself
c.execute('DELETE FROM rating WHERE subjectCode=?', ('MSZ1',))
# -- make codes uniform for judges
c.execute(
    'UPDATE rating SET subjectCode=? WHERE subjectCode=?', ('SK02', 'SK_02'))
c.execute(
    'UPDATE rating SET subjectCode=? WHERE subjectCode=?', ('SK05', 'sk05'))

# -- remove subjects not in the BIDS dataset
layout = BIDSLayout(SOURCE_DIR)
subjects = layout.get_subjects()
subject_codes = ['MOVREST_{}'.format(s) for s in subjects]

placeholder = ','.join(['?' for s in subjects])
c.execute(
    'DELETE FROM ratingExp WHERE subjectCode NOT IN ({})'.format(placeholder),
    subject_codes)

# -- fix the column order
"""
column order was incorrect when inserting; [value] -went into-> [column]:
valence -> known
arousal -> valence
known -> arousal
"""

c.execute('CREATE TEMPORARY TABLE ratingTMP ('
          'subjectCode text, stimulus text, known text, valence int, '
          'arousal int, fear int, happiness int, sadness int, ero int)')

c.execute('INSERT INTO ratingTMP SELECT subjectCode, stimulus, arousal, '
          'known, valence, fear, happiness, sadness, ero FROM ratingEXP')

c.execute('DROP TABLE ratingEXP')
c.execute('CREATE TABLE ratingEXP AS SELECT * FROM ratingTMP')
c.execute('DROP TABLE ratingTMP')

conn.commit()
conn.close()
