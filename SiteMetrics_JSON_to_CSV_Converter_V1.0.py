'''-------------------------------------------------------------------------
Script Name:      Site Metrics' JSON to CSV Converter
Version:          1.0
Description:      This tool automates the conversion of the ER Sites Metrics'
                    JSON files into CSV file formats.
Created By:       Kusasalethu Sithole
Created Date:     2020-08-12
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-08-12
-------------------------------------------------------------------------'''

print("\n\nTOOL - Site Metrics' JSON to CSV Converter")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.")


#Import Libraries
import datetime
import os
import pandas as pd
import pathlib
import time as t


#---------------------------------------Declaring Input Data----------------------------------------------------------------------
## Target json input
json_file = input("\nAbsolute path of the target json file (MANDATORY): ")
if json_file == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target json file according to request above.")
    t.sleep(10)
    exit()
if not os.path.isfile(json_file):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the json file actually exists.")
    t.sleep(10)
    exit()

json_df = pd.read_json (json_file)   # Load the json input file
json_name = os.path.basename(json_file) # capturing just the name of the json input
    

#-----------------------------------------------Preparing the environment---------------------------------------------
os.chdir(pathlib.Path(json_file).parent.absolute())


#---------------------------Defining custom functions------------------
def currentSecondsTime():
    """ Returns the current time in seconds"""
    return int(t.time())

def timeTaken(startTime, endTime):
    """ Returns the difference between a start time and an end time
        formatted as 00:00:00 """
    timeTaken = endTime - startTime
    return str(datetime.timedelta(seconds=timeTaken))

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


#--------------------------------------------------STEP 1: Deriving the target columns and creating the output csv template---------------------------------------------
print("\nStep 1: Deriving the target columns from your " + json_name + " file and creating the output csv template.")

target_columns = []

for column in json_df['columnHeader']['dimensions']:
    target_columns.append(str(column.rsplit(':')[1]))
len_col1 = len(json_df['columnHeader']['dimensions'])
    
for column in json_df['columnHeader']['metricHeader']['metricHeaderEntries']:
    target_columns.append(column['name'].rsplit(':')[1])
len_col2 = len(json_df['columnHeader']['metricHeader']['metricHeaderEntries'])
    
output_csv = pd.DataFrame(columns=target_columns)

print("len_col1:" + str(len_col1),"len_col2:" + str(len_col2))

#--------------------------------------------------STEP 2: Populating the csv template and saving data as csv file format---------------------------------------------
print("\nStep 2: Populating the csv template and saving data as csv file format.")

if len_col1 == 5 and len_col2 == 6:
    for row in json_df['data']['rows']:
        output_csv = output_csv.append(pd.DataFrame([[
        row['dimensions'][0],
        row['dimensions'][1],
        row['dimensions'][2],
        row['dimensions'][3],
        row['dimensions'][4],
        row['metrics'][0]['values'][0],
        row['metrics'][0]['values'][1],
        row['metrics'][0]['values'][2],
        row['metrics'][0]['values'][3],
        row['metrics'][0]['values'][4],
        row['metrics'][0]['values'][5]
    ]], columns=target_columns), ignore_index=True)
elif len_col1 == 6 and len_col2 == 6:
    for row in json_df['data']['rows']:
        output_csv = output_csv.append(pd.DataFrame([[
        row['dimensions'][0],
        row['dimensions'][1],
        row['dimensions'][2],
        row['dimensions'][3],
        row['dimensions'][4],
        row['dimensions'][5],
        row['metrics'][0]['values'][0],
        row['metrics'][0]['values'][1],
        row['metrics'][0]['values'][2],
        row['metrics'][0]['values'][3],
        row['metrics'][0]['values'][4],
        row['metrics'][0]['values'][5]
    ]], columns=target_columns), ignore_index=True)
elif len_col1 == 4 and len_col2 == 5:
    for row in json_df['data']['rows']:
        output_csv = output_csv.append(pd.DataFrame([[
        row['dimensions'][0],
        row['dimensions'][1],
        row['dimensions'][2],
        row['dimensions'][3],
        row['metrics'][0]['values'][0],
        row['metrics'][0]['values'][1],
        row['metrics'][0]['values'][2],
        row['metrics'][0]['values'][3],
        row['metrics'][0]['values'][4]
    ]], columns=target_columns), ignore_index=True)
elif len_col1 == 5 and len_col2 == 5:
    for row in json_df['data']['rows']:
        output_csv = output_csv.append(pd.DataFrame([[
        row['dimensions'][0],
        row['dimensions'][1],
        row['dimensions'][2],
        row['dimensions'][3],
        row['dimensions'][4],
        row['metrics'][0]['values'][0],
        row['metrics'][0]['values'][1],
        row['metrics'][0]['values'][2],
        row['metrics'][0]['values'][3],
        row['metrics'][0]['values'][4]
    ]], columns=target_columns), ignore_index=True)

output_csv_file_name = json_file[:-5] + ".csv"
output_csv.to_csv(output_csv_file_name)

endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
print("\n\nProcess completed. Please refer to your output files in the directory: " + str(pathlib.Path(json_file).parent.absolute()) + ".")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))


