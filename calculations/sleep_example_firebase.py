import pandas as pd
import datetime
from firebase.clear_folder import clear_folder
from fitbit_mongodb.get_fitbit_tokens import auth2_client


# GET DATA
def get_data(start_n_days_back,end_n_days_back):
    for number in range(start_n_days_back,end_n_days_back):
        day = str((datetime.datetime.now() - datetime.timedelta(days=number)).strftime("%Y-%m-%d"))
        today = str(datetime.datetime.now().strftime("%Y%m%d"))

        fit_statsSl = auth2_client.sleep(date=day)
        stime_list = []
        sval_list = []
        try:
            print(fit_statsSl['sleep'][0]['minuteData'])
            for i in fit_statsSl['sleep'][0]['minuteData']:
                try:
                    stime_list.append(i['dateTime'])
                    sval_list.append(i['value'])
                except Exception as e:
                    pass
        except Exception as e:
            pass
        sleepdf = pd.DataFrame({'State': sval_list,
                                'Time': stime_list})
        sleepdf['Interpreted'] = sleepdf['State'].map({'2': 'Awake', '3': 'Very Awake', '1': 'Asleep'})
        sleepdf.to_csv('./sleep/' + \
                       day + '.csv', \
                       columns=['Time', 'State', 'Interpreted'], header=True,
                       index=False)
        return sleepdf

if __name__ == '__main__':
    start_n_days_back = 7
    end_n_days_back = 14
    clear_folder("./sleep")
    sleepdf = get_data(start_n_days_back, end_n_days_back)
    print(sleepdf.describe())