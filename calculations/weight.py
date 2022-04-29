import pandas as pd
from definitions import ROOT_DIR
from firebase.firebase_connection import get_from_firebase, get_list_files
import os

# GET DATA
def get_data(start_date,end_date):
    list_files = get_list_files()
    file= "weight.csv"
    if list_files == None:
        print("Files could not be retrieved from firebase, check 'get_list_files' method in firebase/firebase_connection.py")
    elif file not in list_files:
        print("Add openscale datafile renamed to weight.csv to your firebase database")
    else:
        get_from_firebase(file, file)
    path = ROOT_DIR+"/firebase/"+file
    df = pd.read_csv(path, index_col=None, header=0)
    df['dateTime'] = pd.to_datetime(df['dateTime'])
    df = df.groupby(df.dateTime.dt.date).mean()
    df=df.reset_index()
    try:
        os.remove(os.path.join(ROOT_DIR,"calculations", file))
    except Exception as e:
        print(e)
    return df

def weight_data(start_date, end_date):
    start_date,end_date = "_","_"
    # start_date = parser.parse(start_date)
    # end_date = parser.parse(end_date)
    df = get_data(start_date,end_date)
    return df

if __name__ == '__main__':
    df = weight_data("_","_")
    # df.to_csv("weight.csv")
    print(df.columns)
    print(df)