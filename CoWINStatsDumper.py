import datetime
import json
import logging
import time
import os
import pandas as pd
import requests

INDIA_URL = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports"
STATE_URL = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id="
DISTR_URL = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id=&district_id="

#START_DATE = datetime.date(2021, 4, 11)
START_DATE = datetime.date(2021, 3, 14)
#START_DATE = datetime.date(2021, 3, 21)
END_DATE  = datetime.date(2021, 4, 18)
SKIP_STATES = False
SKIP_DISTRICTS = False

def saveResponse(name, json_data):
    with open(name + '.json', 'w') as json_file:
        json.dump(json_data, json_file)

def getDistrictLevelData():
    for day in pd.date_range(start=START_DATE.strftime('%Y-%m-%d'), end=END_DATE.strftime('%Y-%m-%d')):
        for state in range(1,38):
            state_data = {}
            distlist = []
            if not (os.path.isfile('CoWIN_IN_' + str(state) + '_' + day.strftime('%Y-%m-%d') +'.json')):
                logging.info('Skipping' + str(state) + ' for ' + day.strftime('%Y-%m-%d') + ' as no data file exists')
                continue
            with open('CoWIN_IN_' + str(state) + '_' + day.strftime('%Y-%m-%d') +'.json','r') as f1:
                state_data = json.load(f1)
            distlist = [x['district_id'] for x in state_data['getBeneficiariesGroupBy']]
            for dist in distlist:
                params = {'date': day.strftime('%Y-%m-%d'), 'state_id': state, 'district_id': dist}
                if not (os.path.isfile('CoWIN_IN_' + str(state) + '_' + str(dist) + '_' + day.strftime('%Y-%m-%d') + '.json')):
                    try:
                        r = requests.get(url=INDIA_URL, params=params)
                        saveResponse('CoWIN_IN_' + str(state) + '_' + str(dist) + '_' + day.strftime('%Y-%m-%d'), r.json())
                    except:
                        logging.info('Error getting state ' + str(state) + ' district ' + str(dist) + ' data for ' + day.strftime('%Y-%m-%d'))
                else:
                    continue

def main():
    logging.info('====Start CoWIN stats====')
    for day in pd.date_range(start=START_DATE.strftime('%Y-%m-%d'), end=END_DATE.strftime('%Y-%m-%d')):
        params = {'date': day.strftime(
            '%Y-%m-%d'), 'state_id': '', 'district_id': ''}
        if not (os.path.isfile('CoWIN_' + day.strftime('%Y-%m-%d') + '.json')):
            try:
                r = requests.get(url=INDIA_URL, params=params)
                saveResponse('CoWIN_' + day.strftime('%Y-%m-%d'), r.json())
            except:
                logging.debug('Error ')
        if not SKIP_STATES:
            for state_id in range(1, 38):
                params['state_id'] = str(state_id)
                if not (os.path.isfile('CoWIN_IN_' + params['state_id'] + '_' + day.strftime('%Y-%m-%d') + '.json')):
                    try:
                        r = requests.get(url=INDIA_URL, params=params)
                        saveResponse(
                            'CoWIN_IN_' + params['state_id'] + '_' + day.strftime('%Y-%m-%d'), r.json())
                    except:
                        logging.debug('Error saving state ' +
                                    params['state_id'] + 'for date' + params['date'])
                        continue
                continue
    if not SKIP_DISTRICTS:
        getDistrictLevelData()


if __name__ == "__main__":
    logging.basicConfig(filename='CoWINStats_' + time.strftime("%Y%m%d-%H%M%S") +
                        '.log', format='%(asctime)s %(message)s', level=logging.INFO)
    main()
