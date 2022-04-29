import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil import parser
import numpy as np
from fitbit_mongodb.connect_mongodb import mongodb_client
c = mongodb_client.fitbit
c = c.heart

def convert_to_datetime(date):
    return parser.parse(date)


def get_data(day_date):
    d = [i for i in c.find({'activities-heart.dateTime': day_date})]
    if len(d) ==0:
        return pd.DataFrame()
    d= d[0]
    time_list,val_list,date_list = [], [], []
    for i in d['activities-heart-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
        date_list.append(day_date)
    heartdf = pd.DataFrame({ 'day': date_list, 'Heart Rate': val_list, 'Time': time_list})
    return heartdf


def summary_stats(df, col_name):  # function to provide median, min, and max of data
    df = pd.DataFrame({'Mean ': str(round(np.mean(df[col_name]), 2)),
                       'Median': str(np.median(df[col_name])),
                       'Min': str(np.min(df[col_name])),
                       'Max': str(np.max(df[col_name]))}, index=[0])
    return df


def heartrate_data(start_date, end_date):
    # filter on date
    start_date = parser.parse(start_date)
    end_date = parser.parse(end_date)
    HR = pd.DataFrame(columns=['Heart Rate', 'Time'])
    diff_date = (end_date - start_date).days
    # loop to get data from db
    for i in range(0,(diff_date+1)):
        day = str(start_date.date()+timedelta(i))
        heartrate_new = get_data(day)
        if not heartrate_new.empty:
            HR = HR.append(heartrate_new)
    # add summary stats
    df_summary_stats = summary_stats(HR, 'Heart Rate')
    return HR, df_summary_stats


if __name__ == '__main__':
    date_now = dt.now()
    start_date = date_now - timedelta(5)
    HR, df_summary_stats = heartrate_data(str(start_date), str(date_now))
    print(HR)
    print(df_summary_stats)