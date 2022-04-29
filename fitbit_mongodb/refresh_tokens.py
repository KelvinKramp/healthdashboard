# most of this is copied from: https://github.com/anujk3/fitbit-project/blob/111f79abdda94a1c73b3172437bd33b0ad937d5e/fitbit.py

import os, base64, requests, urllib
import json
from definitions import ROOT_DIR
from fitbit_mongodb.connect_mongodb import mongodb_client

def get_fresh_tokens():
    path = ROOT_DIR+"/secrets.json"
    if os.path.isfile(path):
        "Converting json file into environment variables"
        with open(path) as read_file:
            read_file = read_file.read()
            secret = json.loads(str(read_file))
        os.environ["CLIENT_ID"] = secret["CLIENT_ID"]
        os.environ["CLIENT_SECRET"] = secret["CLIENT_SECRET"]
        os.environ["REFRESH_TOKEN"] = secret["REFRESH_TOKEN"]
        try:
            os.remove(path)
        except Exception as e:
            print(e)
    else:
        "Refreshing database based on environment variables"
    CLIENT_ID = os.environ["CLIENT_ID"]
    CLIENT_SECRET = os.environ["CLIENT_SECRET"]
    REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
    # Construct the authentication header
    data_string = CLIENT_ID + ':' + CLIENT_SECRET
    data_bytes = data_string.encode("utf-8")
    auth_header = base64.b64encode(data_bytes)
    headers = {
        'Authorization': 'Basic %s' % str(auth_header)[2:-1],
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Set up parameters for refresh request
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN
    }

    # Place request
    resp = requests.post('https://api.fitbit.com/oauth2/token', data=params, headers=headers)

    status_code = resp.status_code
    resp = resp.json()

    if status_code != 200:
        raise Exception(
            "Something went wrong refreshing (%s): %s" % (resp['errors'][0]['errorType'], resp['errors'][0]['message']))

    # Distil
    ACCESS_TOKEN = resp['access_token']
    REFRESH_TOKEN = resp['refresh_token']

    json_data = {}
    json_data["CLIENT_ID"] = CLIENT_ID
    json_data["CLIENT_SECRET"] = CLIENT_SECRET
    json_data["ACCESS_TOKEN"] = ACCESS_TOKEN
    json_data["REFRESH_TOKEN"] = REFRESH_TOKEN
    fitbit_db = mongodb_client.fitbit
    collection_name = "client_info"
    fitbit_db_client_info = fitbit_db[collection_name]
    fitbit_db_client_info.insert_many([json_data])

    return CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN, REFRESH_TOKEN


if __name__ == '__main__':
    a,b,c,d = get_fresh_tokens()
    print("CLIENT_ID")
    print(a)
    print("CLIENT SECRET")
    print(b)
    print("ACCESS_TOKEN")
    print(c)
    print("REFRESH_TOKEN")
    print(d)