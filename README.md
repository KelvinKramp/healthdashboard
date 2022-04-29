# Health Dashboard
Health dashboard in Dash. Uses data from FitBit, NightScout and OpenScale.

## Screenshot
![alt text](images/screenshothealthdashboard.png)


## Demo
https://health--dashboard.herokuapp.com/hr-compare

## Overview
![alt text](images/Healthdashboardoverview.png)

## Preperation

Follow this tutorial to create mongoDB database (when choosing username and password use only letters to prevent difficulties in connecting with the database later):
https://codingandfun.com/store-financial-data-into-a-mongodb-database/

Follow Stephen Hsu's tutorial to create fitbit developer access and get clientid, clientsecret, accestoken and refreshtoken:
https://towardsdatascience.com/collect-your-own-fitbit-data-with-python-ff145fa10873

## Installation

Copy this respository to your local harddrive.

```bash
git clone https://github.com/KelvinKramp/health-dashboard.git
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary modules.

```bash
pip install requirements.txt
```


Add cliend_id and client_secret to new file with name "secrets.json" in config directory with format:
```bash
    {"CLIENT_ID":"XXXX",
    "CLIENT_SECRET":"12345XXXX12345xxxxx"}
    """)
```

Add new file with name "connection_string.py" in config directory with mongo DB connection string from the first tutorial in format:
```bash
connection_string = "mongodb+srv://USERNAME:PASSWORD@cluster0.boaqd.mongodb.net/database?retryWrites=true&w=majority"
```

Write config info from firebase account in .env file in folder firebase (/config/.env):
   ```bash
config='{"serviceAccount": "serviceaccount.json","apiKey": "xxx","authDomain": "xxx.firebaseapp.com"....")'
```

Store serviceaccount.json file in root directory. 

When uploading to Heroku read notes/bugs.txt to prevent getting syntax error. 
There is a line in the Crypto module 
   ```bash
s = pack('>I', n & 0xffffffff) + s
```
that gets changed to
   ```bash
s = pack('>I', n & 0xffffffffL) + s
 ```
after uploading to Heroku for some strange reason :-( 


## Usage

```python
python main.py
```
## Weight

For weight, BMI, fatpercentage, etc. assessment copy csv file with weights and name "weight.csv" to your firebase database.


## To do
* Incorporate glucose levels from freestyle libre via xdrip.
* Incorporate fitness activity.

## Sources used
Open humans data tool: <br>
https://github.com/danamlewis/OpenHumansDataTools

Nightscout to Open Humans Data Transfer Tool: <br>
https://github.com/NightscoutFoundation/dataxfer

Fitbit module:<br>
https://github.com/orcasgit/python-fitbit.readthedocs

Fitbit API Python Client Implementation
For documentation: http://python-fitbit.readthedocs.org/

Application register page<br>
https://dev.fitbit.com/apps/details/23BJM5

More detailed information python fitbit api: <br>
https://python-fitbit.readthedocs.io/en/latest/#fitbit-api

Youtube video <br>
https://www.youtube.com/watch?v=5SXW7oP8DGE 

Stackoverflow post about refreshing access tokens<br>
https://stackoverflow.com/questions/37651759/refreshing-access-token-for-fitbit

Fitbit community post about refreshing access tokens<br>
https://community.fitbit.com/t5/Web-API-Development/How-to-refresh-access-token-with-refresh-token-Python/td-p/2865665

Fitbit Data Exploration and its Relation to Real Events  by Stephen Hsu 


## Contact
You find my contact info over [here](https://www.kelvinkramp.com/contact-9).
