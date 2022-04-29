import pandas as pd
import numpy as np
from datetime import timedelta
import plotly.express as px
from dateutil import parser
from definitions import ROOT_DIR
from firebase.firebase_connection import get_from_firebase, get_list_files
import datetime
import os

# GET DATA
def get_data(start_date,end_date):
    list_files = get_list_files()
    if list_files == None:
        print("files could not be retrieved from firebase,check firebase get list files method")
        return None
    list_files_2=[]
    for i in list_files:
        try:
            date = parser.parse(i[-14:-4])
            if start_date <= date <= end_date:
                list_files_2.append(i)
        except Exception as e:
            continue
    csvs = [d for d in list_files_2 if d[-4:] == ".csv"]
    list_ = []
    for c in csvs:
        get_from_firebase(c,c)
        c = ROOT_DIR+"/firebase/"+c
        df = pd.read_csv(c, index_col=None, header=0)
        os.remove(c)
        df['date'] = c[-14:-4]
        df['date'] = pd.to_datetime(df['date'])
        df.loc[:, 'Date'] = pd.to_datetime(df.date.astype(str) + ' ' + df.Time.astype(str))
        year, month, day = int(c[-14:-10]),int(c[-9:-7]),int(c[-6:-4])
        df['year'] = year
        df['month'] = month
        df['day'] = day
        df['DOW'] = datetime.date(year, month, day).strftime("%A")
        df['DOW'] = pd.Categorical(df['DOW'],
                    categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)
        list_.append(df)
    frame = pd.concat(list_)
    frame = frame.drop(['Time', 'date'], axis=1)
    frame = frame.sort_values(by='Date')
    frame = frame.set_index("Date")
    return frame


def summary_stat(df, col_name):  # function to provide median, min, and max of data
    df = pd.DataFrame({'Mean ': str(round(np.mean(df[col_name]), 2)),
                       'Median': str(np.median(df[col_name])),
                       'Min': str(np.min(df[col_name])),
                       'Max': str(np.max(df[col_name]))}, index=[0])
    return df


def heart_rate_date_filter(start_date, end_date, frame):
    # filter on date
    frame = frame.loc[start_date:(end_date+timedelta(1))][:-1]
    # create HR-df
    HR = pd.DataFrame()
    HR['Heart Rate'] = frame['Heart Rate']
    HR['day'] = frame['day']
    return HR

def heart_rate_data(start_date, end_date):
    start_date = parser.parse(start_date)
    end_date = parser.parse(end_date)
    # print(start_date,end_date)
    frame = get_data(start_date,end_date)
    HR = heart_rate_date_filter(start_date, end_date, frame)
    df_summary_stats = summary_stat(HR, 'Heart Rate')
    return HR, df_summary_stats

if __name__ == '__main__':
    HR, df_summary_stats = heart_rate_data("2021-12-18", "2021-12-20")
    title = "HR from {} to {} ".format("2021-12-19", "2021-12-20")
    fig = px.histogram(HR, x="Heart Rate",nbins=26, range_x=[50, 180], title=title,)
    fig.update_layout(bargap=0.2)
    fig.show()
    # fig2 = px.box(HR, x="day", y="Heart Rate", points="all")
    # fig2.show()
    # fig2 = heart_rate_main(10, 18)
    # fig2.show()
