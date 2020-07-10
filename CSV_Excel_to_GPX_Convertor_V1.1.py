'''-------------------------------------------------------------------------
Script Name:      CSV/Excel to GPX Converter
Version:          1.1
Description:      This tool automates the conversion of csv or excel files
                    into gpx file format.
                  file format.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-08
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-07-09
-------------------------------------------------------------------------'''

print("\n\nTOOL - CSV/Excel to GPX Converter")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas, gpx_converter and xlrd libraries are installed using your pip package (i.e. from your terminal run 'pip install pandas gpx_converter xlrd'.")


#Import Libraries
import pandas as pd
import time
import os
import pathlib
import datetime
from gpx_converter import Converter


#---------------------------------------Declaring Data Paths and target fields----------------------------------------------------------------------
## Target csv/excel input
target_file = input("Absolute path of the target csv/excel file: ")
if target_file == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target csv/excel according to request above.")
    time.sleep(10)
    exit()
if not os.path.isfile(target_file):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    time.sleep(10)
    exit()

if os.path.splitext(target_file)[1] == '.csv':
    target_spreadsheet =  pd.read_csv(target_file)   # Load the csv input file
    target_file_name = os.path.basename(target_file) # capturing just the name of the csv input
elif '.xlsx' or '.xls':
    target_spreadsheet =  pd.read_excel(target_file)   # Load the excel input file
    target_file_name = os.path.basename(target_file) # capturing just the name of the excel input
else:
    print("\nPlease ensure that your absolute path refer to either a .csv, .xlsx or .xls file.")
    
## Target field inputs
print("\n\nThe existing fields in this table are:")
for column in target_spreadsheet.columns:
    print("\t " + str(column))

## Longitude field input
longitude_field = input("Please state the exact name of the longitude field in your csv/excel file: ")
if longitude_field == "":
    print("REMINDER: When running this tool, remember to specify the name of the longitude field according to request above.")
    time.sleep(10)
    exit()
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == longitude_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the field name provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        time.sleep(10)
        exit()

## Latitude field input
latitude_field = input("Please state the exact name of the latitude field in your csv/excel file: ")
if latitude_field == "":
    print("REMINDER: When running this tool, remember to specify the name of the latitude field according to request above.")
    time.sleep(10)
    exit()
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == latitude_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the field name provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        time.sleep(10)
        exit()

## Datetime field input
datetime_field = input("Please state the exact name of the datetime field in your csv/excel file: ")
if datetime_field == "":
    print("REMINDER: When running this tool, remember to specify the name of the datetime field according to request above.")
    time.sleep(10)
    exit()
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == datetime_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the field name provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        time.sleep(10)
        exit()


#-----------------------------------------------Preparing the environment---------------------------------------------
os.chdir(pathlib.Path(target_file).parent.absolute())


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


startTime = currentSecondsTime()


#--------------------------------------------------STEP 1: Create a table using only the target fields---------------------------------------------
print("\nStep 1: Create a table using only the target fields - " + longitude_field + ", " + latitude_field + ", " + datetime_field + " - from your " + target_file_name + " file.")
extracted_csv = pd.DataFrame()
extracted_csv["Latitude"] = target_spreadsheet[latitude_field]
extracted_csv["Longitude"] = target_spreadsheet[longitude_field]
extracted_csv["Datetime"] = target_spreadsheet[datetime_field]


#--------------------------------------------------STEP 2: Save the extracted table as gpx file format---------------------------------------------
print("\nStep 2: Save the extracted table as gpx file format.")
extracted_csv_file_name = target_file_name[:-4] + "_extract.csv"
extracted_csv.to_csv(extracted_csv_file_name)

gpx_file_name = target_file_name[:-4] + "_extract.gpx"
Converter(input_file=extracted_csv_file_name).csv_to_gpx(lats_colname=latitude_field, longs_colname=longitude_field, output_file=gpx_file_name)


endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
print("\n\nProcess completed. Please refer to your output files in the directory: " + str(pathlib.Path(target_file).parent.absolute()) + ".")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))
