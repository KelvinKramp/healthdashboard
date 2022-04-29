import pandas as pd
# from pandasgui import show
from definitions import ROOT_DIR
import os

def convert_json_to_pickle(filename="glucose_values.json"):
    out_file = open(filename, "r")
    data = out_file.read()
    out_file.close()
    data = data.replace("false","False")
    data = data.replace("true","True")
    df = pd.DataFrame(eval(data))
    df.to_pickle(os.path.join(ROOT_DIR, "data", "gluc_values.pkl"))


def get_df(filename="gluc_values.pkl"):
    df = pd.read_pickle(os.path.join(ROOT_DIR, "data",filename))
    df = df[["dateString", "date", "sgv"]]
    df = df.dropna()
    # if len(df)> 100000:
    #     df = df[-43800:-1]
    df['dateString'] = pd.to_datetime(df['dateString'], utc=True)
    # try:
    #     df['dateString'] = df['dateString'].astype('datetime64[ns]')
    # except Exception as e:
    #     print(e)
    #     df['dateString'] = pd.to_datetime(df['dateString'], utc=True)
    return df

if __name__ == "__main__":
    import time
    start = time.time()
    convert_json_to_pickle(filename="glucose_values_old.json")
    df = get_df()
    end = time.time()
    print(end-start)
