from firebase.firebase_connection import get_list_files
import fitbit
import gather_keys_oauth2 as Oauth2
from datetime import timedelta
import pandas as pd
import firebase.firebase_connection as fc
from datetime import datetime as dt
import os
import json
from definitions import env_path

if os.path.exists(env_path):
    # if info stored in .env file
    from dotenv import dotenv_values
    config = dotenv_values(env_path)
    # get configuration settings firebase
    CLIENT_ID = config['CLIENT_ID']
    CLIENT_SECRET = config['CLIENT_SECRET']
    detail_level = config['detail_level']
    config = config["config"]
else:
    # if info stored as heroku environment variables
    CLIENT_ID = os.environ['CLIENT_ID']
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    detail_level = os.environ['detail_level']
    config = os.environ['config']

# convert configurations string into json format
config = json.loads(config)

def store_data_fitbit_on_firebase(start_date, end_date):
    # CHECK IF FILES ALREADY STORED ON FIREBASE
    list_files = get_list_files()
    if any(str(start_date.date()) in f for f in list_files):
        if any(str(end_date.date()) in f for f in list_files):
            return

    # AUTHENTICATION
    server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()
    ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
    auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                                 refresh_token=REFRESH_TOKEN)

    # GET DATA
    diff_date = (end_date - start_date).days
    for i in range(0,(diff_date+1)):
        day = str(start_date.date()+timedelta(i))
        fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=day, detail_level=detail_level)
        time_list = []
        val_list = []
        for i in fit_statsHR['activities-heart-intraday']['dataset']:
            val_list.append(i['value'])
            time_list.append(i['time'])
        heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
        file_name = 'heart' + day + '.csv'
        heartdf.to_csv(file_name,
                       columns=['Time', 'Heart Rate'], header=True,
                       index=False)
        fc.store_on_firebase(file_name, file_name)
        print("file ", file_name, "succesfully stored on firebase")
        os.remove(file_name)
        print("file succesfully removed from local disk")

if __name__ == '__main__':
    date_now = dt.now()
    start_date = date_now - timedelta(30)
    store_data_fitbit_on_firebase(start_date, date_now)