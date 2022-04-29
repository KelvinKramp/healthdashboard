import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil import parser
from fitbit_mongodb.connect_mongodb import mongodb_client
c = mongodb_client.fitbit
c = c.sleep

def convert_to_datetime(date):
    return parser.parse(date)


def get_data(day_date):
    d = [i for i in c.find({'sleep.dateOfSleep': day_date})]
    if len(d) ==0:
        return pd.DataFrame()
    d= d[0]
    date, stages, totalMinutesAsleep, totalTimeInBed, efficiency, startTime, endTime = {},{},{},{},{},{},{}
    date["date"] = d["sleep"][0]['dateOfSleep']
    stages = d["summary"]['stages']
    totalMinutesAsleep["totalMinutesAsleep"] = d["summary"]['totalMinutesAsleep']
    totalTimeInBed["totalTimeInBed"] = d["summary"]['totalTimeInBed']
    efficiency["efficiency"] = d["sleep"][0]['efficiency']
    startTime['startTime'] = d["sleep"][0]['startTime']
    endTime['endTime'] = d["sleep"][0]['endTime']
    d = {**date, **stages, **totalMinutesAsleep, **totalTimeInBed, **efficiency, **startTime, **endTime}
    df = pd.DataFrame.from_records([d])
    return df


def sleep_data(start_date, end_date):
    # filter on date
    start_date = parser.parse(start_date)
    end_date = parser.parse(end_date)
    sleepdata = pd.DataFrame(columns=['date', 'deep', 'light', 'rem', 'wake', 'totalMinutesAsleep',
                          'totalTimeInBed', 'efficiency', 'startTime', 'endTime'])
    diff_date = (end_date - start_date).days
    for i in range(0,(diff_date+1)):
        day = str(start_date.date()+timedelta(i))
        sleepdata_new = get_data(day)
        if not sleepdata_new.empty:
            sleepdata = sleepdata.append(sleepdata_new)
    return sleepdata


if __name__ == '__main__':
    date_now = dt.now()
    start_date = date_now - timedelta(5)
    df = sleep_data(str(start_date), str(date_now))
    print(df)