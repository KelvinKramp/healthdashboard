import pyrebase
import os
import json
from definitions import ROOT_DIR, env_path

if os.path.exists(env_path):
    from dotenv import dotenv_values
    config = dotenv_values(env_path)
    config = config["config"]
else:
    config = os.environ['config']


config = json.loads(config)


def store_on_firebase(file_name, file_name_cloud):
    try:
        file_path = ROOT_DIR + "/firebase/" + file_name
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        storage.child(file_name_cloud).put(file_path)
    except Exception as e:
        print("Could not store file ",file_name,"on firebase")
        print(e)


def get_from_firebase(file_name_cloud, file_name_download):
    try:
        file_name_download = ROOT_DIR + "/firebase/" + file_name_download
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        s = storage.child(file_name_cloud)
        s.download(file_name_download)
    except Exception as e:
        print("Could not download file ",file_name_cloud," from firebase")
        print(e)

def get_list_files():
    try:
        firebase = pyrebase.initialize_app(config)
        storage = firebase.storage()
        l = storage.list_files()
        list_files = [i.name for i in l]
        print("file names succesfully retrieved from firebase")
        return list_files
    except Exception as e:
        print(os.getcwd())
        print("Could not retrieve file names from firebase ")
        print(e)
        return None

if __name__ == "__main__":
    print(config)
    list_files = get_list_files()
    print(list_files)
