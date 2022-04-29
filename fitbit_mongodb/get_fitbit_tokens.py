import fitbit
import gather_keys_oauth2 as Oauth2
import json
from definitions import ROOT_DIR
from fitbit_mongodb.connect_mongodb import mongodb_client

# GET CLIENT INFO FROM JSON FILE
try:
    with open(ROOT_DIR + "/secrets.json", "r") as read_file:
        read_file = read_file.read()
        secret = json.loads(str(read_file))
    CLIENT_ID = secret["CLIENT_ID"]
    CLIENT_SECRET = secret["CLIENT_SECRET"]
except Exception as e:
    print("""
    add cliend_id and client_secret to file with name "secrets.json" in  format:
    {"CLIENT_ID":"XXXX",
    "CLIENT_SECRET":"12345XXXX12345xxxxx"}
    """)
    exit()

# GET ACCES AND REFRESH TOKEN THROUGH AUTHENTICATION WITH CLIENT INFO AND THE API MODULE
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)

# STORE CLIENT INFO AND RETRIEVED TOKENS ON MONGODB
json_data = {}
json_data["CLIENT_ID"] = CLIENT_ID
json_data["CLIENT_SECRET"] = CLIENT_SECRET
json_data["ACCESS_TOKEN"] = ACCESS_TOKEN
json_data["REFRESH_TOKEN"] = REFRESH_TOKEN
fitbit_db = mongodb_client.fitbit
collection_name = "client_info"
fitbit_db_client_info = fitbit_db[collection_name]
fitbit_db_client_info.insert_many([json_data])