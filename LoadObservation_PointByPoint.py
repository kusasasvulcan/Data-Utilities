"""--------------------------------------------------------------------------------------------------
Script Name:      Load Observations Point By Point
Version:          1.2
Description:      This tool loads observations of a subject into an ER Site, one by one, using a
                    keyboard trigger.
Created By:       Dennis Schneider 
Created Date:     2020-99-99
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-09-11
---------------------------------------------------------------------------------------------------"""


print("\n\nTOOL - Load Observations Point By Point")


#---------------------------------------Importing Libraries------------------------------------------
import csv
import datetime
import ERModule
import keyboard
import os
import time as t


#---------------------------------------Declaring User Inputs-----------------------------------------
## Target csv input
target_csv = input("\nAbsolute path of the target csv file (MANDATORY): ")
if target_csv == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target csv according to request above.")
    t.sleep(10)
    exit()
if not os.path.isfile(target_csv):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    t.sleep(10)
    exit()

## Target ER Site
SERVER = input("\nPlease state target ER Site Link, i.e. playground.pamdas.org (MANDATORY): ")
if SERVER == "":
    print("REMINDER: When running this tool, remember to specify the target ER Site link according to request above.")
    t.sleep(10)
    exit()

## Access Token
TOKEN = input("\nPlease provide a valid access token for the ER Site you provided above, i.e. 0DeBd8wclNpiLmAMrcPpNjw8wF2yXd (MANDATORY): ")
if TOKEN == "":
    print("REMINDER: When running this tool, remember to specify the access token according to request above.")
    t.sleep(10)
    exit()


#--------------------------------------Defining custom function---------------------------------------
def submitRows(row):
    """ Calls RModule.recordObservation() using the input row's data,
        which uploads the observation into the target ER Site."""
    try:
        recordedAt = datetime.datetime.strptime(row['timestamp'], "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        recordedAt = datetime.datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S.%f%z")
    except KeyError:
        recordedAt = datetime.datetime.now(tz=None)
    recordedAt += datetime.timedelta(hours=2)
    lat = float(row['Lat'])
    lon = float(row['Lng'])
    sourceID = row['deviceId']
    
    additionalData = row
    additionalData.pop('Lat')
    additionalData.pop('Lng')
    additionalData.pop('deviceId')

    ERModule.recordObservation(SERVER, TOKEN, recordedAt, sourceID,
        row['Name'], 'wildlife', 'elephant', 'Tracker', 'tracking_device', lat,
        lon, additionalData)
        

#------------------------------------Compiling the input array---------------------------------------------
print("\nCompiling the input array.")

f = open(target_csv, encoding="utf-8-sig")
reader = csv.DictReader(f, delimiter=',', quotechar='"')

rows = [[],[],[],[],[],[],[],[],[],[]]
i = 0
for row in reader:
    rows[i%10].append(row)
    i = i + 1


#--------------------------------User-triggered uploading of observations--------------------------------------
print("\nUser-triggered uploading of observations. Use your keyboard combination 'shift+g' to trigger observation upload.")
row_index = 0
for row in rows:
    while True and row_index < 3:
        if keyboard.is_pressed('shift+g'):
            row = row[0]
            submitRows (row)
            row_index += 1
            break
        elif keyboard.is_pressed('shift+q'):
            break
        else:
            continue


# ---------------------------End of Process ---------------------------
print("\n\nProcess Complete.")        
