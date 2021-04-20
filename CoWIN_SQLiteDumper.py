import json
import sqlite3
import os.path
import re

DATA_FOLDER = 'data'
INDIA_FILE_NAME = r'CoWIN_2021*.json' #+ date
STATE_FILE_NAME = 'CoWIN_IN_' #state_code + date
DISTRICT_FILE_NAME = 'CoWIN_IN_' #state_code + district_code + date
reg = re.compile(INDIA_FILE_NAME)

india_files = [f for f in os.listdir(DATA_FOLDER) if re.match(r'CoWIN_202[1|2]-[0-9]+.*\.json', f)]
state_files = [f for f in os.listdir(DATA_FOLDER) if re.match(r'CoWIN_IN_[0-9]+_202[1|2]-[0-9]+.*\.json', f)]
district_files = [f for f in os.listdir(DATA_FOLDER) if re.match(r'CoWIN_IN_[0-9]+_[0-9]+_202[1|2]-[0-9]+.*\.json', f)]

