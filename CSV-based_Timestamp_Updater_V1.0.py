'''-------------------------------------------------------------------------------
Script Name:      CSV-based Timestamp Updater
Version:          1.0
Description:      This tool automates the updating of the timestamp data as a
                    spread from the current date (maintaining the scale of spread)
                    in a CSV file.
Created By:       Kusasalethu Sithole
Created Date:     2020-08-20
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-08-20
-------------------------------------------------------------------------------'''


print("\n\nTOOL - CSV-based Timestamp Updater")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.")


#Import Libraries
import datetime as DT
from datetime import datetime
import os
import pandas as pd
import pathlib
import re
import time as t


#---------------------------------------Declaring Data Paths, target fields and target location----------------------------------------------------------------------
## Target csv input
target_file = input("\nAbsolute path of the target csv file (MANDATORY): ")
if target_file == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target csv according to request above.")
    t.sleep(10)
    exit()
if not os.path.isfile(target_file):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the file actually exists.")
    t.sleep(10)
    exit()

target_spreadsheet =  pd.read_csv(target_file)   # Load the csv input file
target_file_name = os.path.basename(target_file) # capturing just the name of the csv input
    
## Target field inputs
for column in target_spreadsheet.columns:
    if re.search('reported_at_\(gmt', column.lower()) or column.lower() == 'date':
        timestamp_field = column

try:
    if timestamp_field is not None:
        pass
except NameError:
    timestamp_field = ""  

## Timestamp field input
if timestamp_field == '':
    print("\n\nWe could not automatically determine the name of your timestamp field. The existing fields in this table are:")
    for column in target_spreadsheet.columns:
        print("\t " + str(column))
    timestamp_field_input = input("\nPlease state the exact name of the timestamp field in your csv file (MANDATORY): ")
    if timestamp_field_input == "" or timestamp_field_input == " ":
        print("REMINDER: When running this tool, remember to specify the name of the timestamp field according to request above.")
        t.sleep(10)
        exit()
    else:
        timestamp_field = timestamp_field_input
        
    field_no = len(target_spreadsheet.columns)
    iter_no = 0
    for field in target_spreadsheet.columns:
        if field == timestamp_field:
            break 
        elif  iter_no < field_no - 1:
            iter_no += 1
            continue
        else:
            print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv file.")
            t.sleep(10)
            exit()        

##Timestamp Notation    
### Date Separator
date_separators = ['/', '-']
if re.search(date_separators[0], target_spreadsheet[timestamp_field][0]):
    date_separation = date_separators[0]
elif re.search(date_separators[1], target_spreadsheet[timestamp_field][0]):
    date_separation = date_separators[1]
else:
    print("The date separator in your timestamp field is not accomodated in this tool. The date notation currently supported is '/' or '-'. You can either change this notation in your csv file OR notify the tool developers about this notification so that they can make accomodation for your date notation.")
    t.sleep(20)
    exit() 
    
### Date-Time Separator
alphabets = 'abcdefghijklmnopqrstuvwxyz'
datetime_separators = ' ' + alphabets + alphabets.upper()
for datetime_separator in datetime_separators:
    if re.search(datetime_separator, target_spreadsheet[timestamp_field][0]):
        datetime_separation = datetime_separator

try:
    if datetime_separation is not None:
        pass
except NameError:
    print("The datetime separator in your timestamp field is not accomodated in this tool. The datetime notation currently supported is a single space or an alphabet character (lower case or upper case). You can either change this notation in your csv file OR notify the tool developers about this notification so that they can make accomodation for your date notation.")
    t.sleep(20)
    exit()

###time_notation
time_char_count = 0
for char in target_spreadsheet[timestamp_field][0]: 
    if char == ':': 
        time_char_count += 1

### Resultant timestamp notation
if date_separation == date_separators[0]:
    if time_char_count == 2:
        timestamp_notation = '%m/%d/%y{}%H:%M:%S'.format(datetime_separation)
    elif time_char_count == 1:
        timestamp_notation = '%m/%d/%y{}%H:%M'.format(datetime_separation)
    elif time_char_count == 0:
        timestamp_notation = '%m/%d/%y{}%H'.format(datetime_separation)
elif date_separation == date_separators[1]:
    if time_char_count == 2:
        timestamp_notation = '%Y-%m-%d{}%H:%M:%S'.format(datetime_separation)
    elif time_char_count == 1:
        timestamp_notation = '%Y-%m-%d{}%H:%M'.format(datetime_separation)
    elif time_char_count == 0:
        timestamp_notation = '%Y-%m-%d{}%H'.format(datetime_separation)
    

## Current Timestamp
current_date = datetime.combine(datetime.today(), datetime.min.time())


#-----------------------------------------------Preparing the environment---------------------------------------------
os.chdir(pathlib.Path(target_file).parent.absolute())


#---------------------------Defining custom functions------------------
def currentSecondsTime():
    """ Returns the current time in seconds"""
    return int(t.time())

def timeTaken(startTime, endTime):
    """ Returns the difference between a start time and an end time
        formatted as 00:00:00 """
    timeTaken = endTime - startTime
    return str(DT.timedelta(seconds=timeTaken))

def showPyMessage(message, messageType="Message"):
    """ Shows a formatted message to the user during processing. """
    if (messageType == "Message"):
        os.system('echo ' + str(t.ctime()) + " - " + message + "'")
        print(message)
    if (messageType == "Warning"):
        os.system('echo ' + str(t.ctime()) + " - " + message + "'")
        print(message)
    if (messageType == "Error"):
        os.system('echo ' + str(t.ctime()) + " - " + message + "'")
        print(message)


startTime = currentSecondsTime()


#--------------------------------------------------STEP 1: Determing the latest timestamp in the csv file---------------------------------------------
print("\nStep 1: Determing the latest timestamp in the " + timestamp_field + " field of your " + target_file_name + " file.")

latest_timestamp = datetime.strptime(target_spreadsheet[timestamp_field].max(), timestamp_notation)

#--------------------------------------------------STEP 2: Determining the deviation for each timestamp from the latest timestamp---------------------------------------------
print("\nStep 2: Determining the deviation for each timestamp from the latest timestamp.")

target_spreadsheet["time_deviation"] = ''

for index, row in target_spreadsheet.iterrows():
    target_spreadsheet.loc[index, "time_deviation"] = datetime.strptime(row[timestamp_field], timestamp_notation) - latest_timestamp

    
#--------------------------------------------------STEP 3: Creating new timestamps using the time deviations from the latest timestamp and the current timestamp---------------------------------------------
print("\nStep 3: Creating new timestamps using the time deviations from the latest timestamp and the current timestamp.")

for index, row in target_spreadsheet.iterrows():    
    target_spreadsheet.loc[index, timestamp_field] = row["time_deviation"] + current_date + (datetime.strptime(row[timestamp_field], timestamp_notation) - datetime.combine(datetime.strptime(row[timestamp_field], timestamp_notation), datetime.min.time()))

target_spreadsheet = target_spreadsheet.drop(columns=["time_deviation"])
    
output_csv_file_name = target_file[:-4] + "_updated.csv"
target_spreadsheet.to_csv(output_csv_file_name, index=False)

endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
print("\n\nProcess completed. Please refer to your output files in the directory: " + str(pathlib.Path(target_file).parent.absolute()) + ".")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))