'''-------------------------------------------------------------------------
Script Name:      CSV/Excel to GPX Converter
Version:          2.1
Description:      This tool automates the conversion of csv or excel files
                    into the custom gpx file format.
                  file format.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-08
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-08-04
-------------------------------------------------------------------------'''

print("\n\nTOOL - CSV/Excel to GPX Converter")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.")


#Import Libraries
import datetime
import os
import pandas as pd
import pathlib
import re
import time as t
import xml.etree.ElementTree as ET


#---------------------------------------Declaring Data Paths and target fields----------------------------------------------------------------------
## Target csv/excel input
target_file = input("\nAbsolute path of the target csv/excel file (MANDATORY): ")
if target_file == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target csv/excel according to request above.")
    t.sleep(10)
    exit()
if not os.path.isfile(target_file):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    t.sleep(10)
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
    if re.search('longitude', column.lower()) or column.lower() == "lon":
        longitude_field = column
    if re.search('latitude', column.lower()) or column.lower() == "lat":
        latitude_field = column
    if re.search('date', column.lower()):
        datetime_field = column
    if re.search('elevation', column.lower()) or re.search('altitude', column.lower()):
        elevation_field = column

## Longitude field input
try:
    print("\nYour longitude fieldname is: " + longitude_field, end="")
    longitude_field_input = input("If we have accurately determined the name of your longitude field, please press enter. If not, please type the correct name: ")
    if longitude_field_input == "" or longitude_field_input == " ":
        print("Longitude fieldname is now verified.")
    else:
        longitude_field = longitude_field_input    
except NameError:
    longitude_field_input = input("We could not automatically determine the name of your longitude field. Please state the exact name of the longitude field in your csv/excel file (MANDATORY): ")
    if longitude_field_input == "" or longitude_field_input == " ":
        print("REMINDER: When running this tool, remember to specify the name of the longitude field according to request above.")
        t.sleep(10)
        exit()
    else:
        longitude_field = longitude_field_input
    
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == longitude_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        t.sleep(10)
        exit()

## Latitude field input
try:
    print("\nYour latitude fieldname is: " + latitude_field, end="")
    latitude_field_input = input("If we have accurately determined the name of your latitude field, please press enter. If not, please type the correct name: ")
    if latitude_field_input == "" or latitude_field_input == " ":
        print("Latitude fieldname is now verified.")
    else:
        latitude_field = latitude_field_input    
except NameError:
    latitude_field_input = input("We could not automatically determine the name of your latitude field. Please state the exact name of the latitude field in your csv/excel file (MANDATORY): ")
    if latitude_field_input == "" or latitude_field_input == " ":
        print("REMINDER: When running this tool, remember to specify the name of the latitude field according to request above.")
        t.sleep(10)
        exit()
    else:
        latitude_field = latitude_field_input
    
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == latitude_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        t.sleep(10)
        exit()

## Datetime field input
try:
    print("\nYour Datetime fieldname is: " + datetime_field, end="")
    datetime_field_input = input("If we have accurately determined the name of your datetime field, please press enter. If not, please type the correct name: ")
    if datetime_field_input == "" or datetime_field_input == " ":
        print("Datetime fieldname is now verified.")
    else:
        datetime_field = datetime_field_input    
except NameError:
    datetime_field_input = input("We could not automatically determine the name of your datetime field. Please state the exact name of the datetime field in your csv/excel file (MANDATORY and format must be YYYY-MM-DD HH:MM:SS): ")
    if datetime_field_input == "" or datetime_field_input == " ":
        print("REMINDER: When running this tool, remember to specify the name of the datetime field according to request above.")
        t.sleep(10)
        exit()
    else:
        datetime_field = datetime_field_input
    
field_no = len(target_spreadsheet.columns)
iter_no = 0
for field in target_spreadsheet.columns:
    if field == datetime_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
        t.sleep(10)
        exit()

## Elevation field input
try:
    print("\nYour Elevation fieldname is: " + elevation_field, end="")
    elevation_field_input = input("If we have accurately determined the name of your elevation field, please press enter. If not, please type the correct name: ")
    if elevation_field_input == "" or elevation_field_input == " ":
        print("Elevation fieldname is now verified.")
    else:
        elevation_field = elevation_field_input    
except NameError:
    elevation_field_input = input("We could not automatically determine the name of your elevation field. Please state the exact name of the elevation field in your csv/excel file (OPTIONAL, if there is none, leave answer as empty by pressing enter): ")
    if elevation_field_input == "" or elevation_field_input == " ":
        elevation_field = ""
    else:
        elevation_field = elevation_field_input
    
field_no = len(target_spreadsheet.columns)
iter_no = 0
if elevation_field != "":
    for field in target_spreadsheet.columns:
        if field == elevation_field:
            break 
        elif  iter_no < field_no - 1:
            iter_no += 1
            continue
        else:
            print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv/excel file.")
            t.sleep(10)
            exit()


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


#--------------------------------------------------STEP 1: Creating a table using only the target fields---------------------------------------------
print("\nStep 1: Creating a table using only the target fields (" + longitude_field + ", " + latitude_field + ", " + datetime_field + ",...) from your " + target_file_name + " file.")
extracted_csv = pd.DataFrame()
extracted_csv["Latitude"] = target_spreadsheet[latitude_field]
extracted_csv["Longitude"] = target_spreadsheet[longitude_field]
extracted_csv["Datetime"] = target_spreadsheet[datetime_field]
if elevation_field == "":
    extracted_csv["Elevation"] = 0.999999999
elif elevation_field != "":
    extracted_csv["Elevation"] = target_spreadsheet[elevation_field]

for index, row in extracted_csv.iterrows():
    datetime_value = str(row["Datetime"])
    if len(datetime_value.split()) > 1:
        date = datetime_value.split()[0]
        time = datetime_value.split()[1]
        try:
            if int(date[-4:]) > 1900 and date[-5:-4] == "/":
                day = date.split("/")[0]
                month = date.split("/")[1]
                year = date.split("/")[2]
                date = year + "-" + month + "-" + day
        except:
            continue
        hour = time.split(":")[0]
        minutes = time.split(":")[1]
        if len(time) < 6:
            time = hour + ":" + minutes + ":00"
        extracted_csv.loc[index, "Datetime"]= date + "T" + time + "Z"

for index, row in extracted_csv.iterrows():
    if str(extracted_csv["Latitude"][0])[1] == "," or str(extracted_csv["Latitude"][0])[2] == "," or str(extracted_csv["Latitude"][0])[3] == ",":
        extracted_csv.loc[index, "Latitude"] = row["Latitude"].replace(",", ".")
        extracted_csv.loc[index, "Longitude"] = row["Longitude"].replace(",", ".")
    else:
        extracted_csv.loc[index, "Latitude"] = str(row["Latitude"])
        extracted_csv.loc[index, "Longitude"] = str(row["Longitude"])    
    if elevation_field != "":
        extracted_csv.loc[index, "Elevation"] = float(row["Elevation"])


#--------------------------------------------------STEP 2: Saving the extracted table as gpx file format---------------------------------------------
print("\nStep 2: Saving the extracted table as gpx file format.")

if target_file[-4] == ".":
    extracted_csv_file_name = target_file[:-4] + "_extract.csv"
    extracted_csv.to_csv(extracted_csv_file_name)
    gpx_file_name = target_file[:-4] + ".gpx"
elif target_file[-5] == ".":
    extracted_csv_file_name = target_file[:-5] + "_extract.csv"
    extracted_csv.to_csv(extracted_csv_file_name)
    gpx_file_name = target_file[:-5] + ".gpx"

#The standard elements
gpx = ET.Element("gpx")
gpx.set("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
gpx.set("xmlns","http://www.topografix.com/GPX/1/1")
gpx.set("xsi:schemaLocation","http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")
gpx.set("version","1.1")
gpx.set("creator","Open GPX Tracker for iOS")
trk = ET.SubElement(gpx, "trk")
trkseg = ET.SubElement(trk, "trkseg")

#Write trkpt attributes and subelement text
row_number = len(extracted_csv["Latitude"])
element_no = 0
for record in extracted_csv["Longitude"]:
    trkpt = ET.SubElement(trkseg, "trkpt")
    trkpt.set("lon",extracted_csv["Longitude"][element_no])
    trkpt.set("lat",extracted_csv["Latitude"][element_no])
    ele = ET.SubElement(trkpt, "ele")
    time = ET.SubElement(trkpt, "time")
    ele.text = str(extracted_csv["Elevation"][element_no])
    time.text =  str(extracted_csv["Datetime"][element_no])
    element_no += 1

tree = ET.ElementTree(gpx)
tree.write(gpx_file_name,encoding="UTF-8",xml_declaration='<?xml version="1.0" encoding="UTF-8"?>')

endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
print("\n\nProcess completed. Please refer to your output files in the directory: " + str(pathlib.Path(target_file).parent.absolute()) + ".")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))
