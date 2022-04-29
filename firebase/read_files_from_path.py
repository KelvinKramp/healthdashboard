import pandas as pd
import datetime
import os
from definitions import ROOT_DIR


def read_files_from_path(path): #function to read files and add date components
    list_ = []
    path = ROOT_DIR+"/files/"+path
    my_dir = os.listdir(path)
    csvs = [d for d in my_dir if d[-4:] == ".csv"]
    for c in csvs:
        df = pd.read_csv(path+c,index_col=None, header=0)
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
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    return frame
