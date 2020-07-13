'''-------------------------------------------------------------------------
Script Name:      Wildlife Movement Drivers
Version:          1.0
Description:      This tool XXXX.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-13
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-07-13
-------------------------------------------------------------------------'''

#Import Libraries
import time
import datetime
import os
import requests
import pandas as pd
from sqlalchemy import create_engine


print("\nTOOL - Wildlife Movement Drivers")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas, sqlalchemy and psycopg2 libraries are installed using your pip package (i.e. from your terminal run 'pip install pandas sqlalchemy psycopg2'.")

#---------------------------Declaring Data Inputs------------------
## ER Site & filters
er_site = input("ER Site (i.e. 'stage'): ")
subject_id = input("Subject id (i.e. '50ae00de-2dde-4df3-88b7-89b5c0e9gd26'): ")
since = input("Time filter (i.e. '2020-06-18T22:00:00.000Z'): ")
authorization_bearer = input("The bearer authorization key (i.e. 'HvwIYDw9e7tmzPPOHt3Zf6jxPy9Sew'): ")

## Imagery filters


## Databases
### Postgres
host = input("Host Address: ")
port = input("Database Server Port: ")
database = input("Database Name: ")
user = input("Username: ")
password = input("User Password: ")
    
postgres_db = create_engine('postgresql://' + user + ':' + password + '@' + host + ':' + port + '/' + database)

### MongoDB


#---------------------------Defining custom functions------------------
def currentSecondsTime():
    """ Returns the current time in seconds"""
    return int(time.time())

def timeTaken(startTime, endTime):
    """ Returns the difference between a start time and an end time
        formatted as 00:00:00 """
    timeTaken = endTime - startTime
    return str(datetime.timedelta(seconds=timeTaken))

def showPyMessage(message, messageType="Message"):
    """ Shows a formatted message to the user during processing. """
    if (messageType == "Message"):
        os.system('echo ' + str(time.ctime()) + " - " + message + "'")
        print(message)
    if (messageType == "Warning"):
        os.system('echo ' + str(time.ctime()) + " - " + message + "'")
        print(message)
    if (messageType == "Error"):
        os.system('echo ' + str(time.ctime()) + " - " + message + "'")
        print(message)


tool_startTime = currentSecondsTime()

# ---------------------------STEP 1: Pulling movement data from ER site---------------------------
print("\nStep 1: Pulling the movement data from the " + er_site + " ER Site for the " + subject_id + " subject.")
S1_startTime = currentSecondsTime()

headers = {
    'authorization': 'Bearer ' + authorization_bearer,
}

params = (
    ('since', since),
)

url = 'https://' + er_site + '.pamdas.org/api/v1.0/subject/' + subject_id + '/tracks/'

response_json = requests.get(url, headers=headers, params=params, json={'key':'value'}).json()

S1_endTime = currentSecondsTime()
showPyMessage(" -- Step completed successfully. Step took {}. ".format(timeTaken(S1_startTime, S1_endTime)))


# ---------------------------STEP 2: Preprocess the ER movement data and import into Postgres database---------------------------
print("\nStep 2: Preprocess the ER movement data and import into Postgres database.")
S2_startTime = currentSecondsTime()

data = response_json['data']

response_df = pd.DataFrame()
response_df['Datetime'] = data['features'][0]['properties']['coordinateProperties']['times']
response_df['Geometry'] = data['features'][0]['geometry']['coordinates']
response_df['Subject Type'] = data['features'][0]['properties']['subject_type']
response_df['Subject Subtype'] = data['features'][0]['properties']['subject_subtype']
response_df['Subject ID'] = data['features'][0]['properties']['id']

response_df.to_sql(str(data['features'][0]['properties']['id']), postgres_db, if_exists = 'replace')

S2_endTime = currentSecondsTime()
showPyMessage(" -- Step completed successfully. Step took {}. ".format(timeTaken(S2_startTime, S2_endTime)))


# ---------------------------STEP 3: Accessing suitable Sentinel imagery from the Google Earth Engine---------------------------
print("\nStep 3: Accessing suitable Sentinel imagery from the Google Earth Engine.")
S3_startTime = currentSecondsTime()
S3_endTime = currentSecondsTime()
showPyMessage(" -- Step completed successfully. Step took {}. ".format(timeTaken(S3_startTime, S3_endTime)))


# ---------------------------STEP 4: Calculate the LULC from imagery and import into MongoDB---------------------------
print("\nStep 4: Calculate the LULC from imagery and import into MongoDB.")
S4_startTime = currentSecondsTime()
S4_endTime = currentSecondsTime()
showPyMessage(" -- Step completed successfully. Step took {}. ".format(timeTaken(S4_startTime, S4_endTime)))


# ---------------------------STEP 5: Apply ML to predict Wildlife movement based on LULC---------------------------
print("\nStep 5: Apply ML to predict Wildlife movement based on LULC.")
S5_startTime = currentSecondsTime()
S5_endTime = currentSecondsTime()
showPyMessage(" -- Step completed successfully. Step took {}. ".format(timeTaken(S5_startTime, S5_endTime)))


tool_endTime = currentSecondsTime()

# --------------------------- End of Process ---------------------------
showPyMessage(" -- Tool completed successfully. Process took {}. ".format(timeTaken(tool_startTime, tool_endTime)))