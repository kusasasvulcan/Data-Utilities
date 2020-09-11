'''-------------------------------------------------------------------------
Script Name:      CSV-based Site Coordinates Relocator
Version:          1.3
Description:      This tool automates the relocation of coordinates in CSV
                    file from one site to another.
Created By:       Kusasalethu Sithole
Created Date:     2020-08-18
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-08-19
-------------------------------------------------------------------------'''

print("\n\nTOOL - CSV-based Site Coordinates Relocator")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.")


#Import Libraries
import datetime
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
    if re.search('9999', column.lower()):
        point_geometry_field = column
    if re.search('longitude', column.lower()) or column.lower() == "lon":
        longitude_field = column
    if re.search('latitude', column.lower()) or column.lower() == "lat":
        latitude_field = column

try:
    if point_geometry_field is not None:
        pass
except NameError:
    point_geometry_field = ''
try:
    if longitude_field is not None:
        pass
except NameError:
    longitude_field = ''
try:
    if latitude_field is not None:
        pass
except NameError:
    latitude_field = ''     


if point_geometry_field != '':
    coordinate_nature = '1'
elif longitude_field != '' or latitude_field != '':
    coordinate_nature = '2'
else:
    coordinate_nature = ''

if coordinate_nature == '':
    coordinate_nature_input = input("We could not automatically determine the geometry fieldtypes used in your file. Does your csv have a point geometry field in the form of 'POINT (25.3657 -34.2568)' OR the separate coordinates fields of latitude and longitude. Enter 1 if your answer is the first choice OR enter 2 if your answer is the second choice (MANDATORY): ")
    if coordinate_nature_input == "" or coordinate_nature_input == " ":
        print("Please enter 1 or 2 based on your decision above.")
        t.sleep(10)
        exit()
    if coordinate_nature_input != '1' and coordinate_nature_input != '2':
        print("Your answer must be either 1 or 2.")
        t.sleep(10)
        exit()
    else:
        coordinate_nature = coordinate_nature_input


if coordinate_nature == '1':
    ## Location field input
    if point_geometry_field == '':
        print("\n\nWe could not automatically determine the name of your point geometry field. The existing fields in this table are:")
        for column in target_spreadsheet.columns:
            print("\t " + str(column))
        point_geometry_field_input = input("\nPlease state the exact name of the point geometry field in your csv file (MANDATORY): ")
        if point_geometry_field_input == "" or point_geometry_field_input == " ":
            print("REMINDER: When running this tool, remember to specify the name of the point geometry field according to request above.")
            t.sleep(10)
            exit()
        else:
            point_geometry_field = point_geometry_field_input
            
        field_no = len(target_spreadsheet.columns)
        iter_no = 0
        for field in target_spreadsheet.columns:
            if field == point_geometry_field:
                break 
            elif  iter_no < field_no - 1:
                iter_no += 1
                continue
            else:
                print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv file.")
                t.sleep(10)
                exit()        
    
    target_spreadsheet['Longitude'] = ''
    target_spreadsheet['Latitude'] = ''
    try:
        for index, row in target_spreadsheet.iterrows():
            target_spreadsheet.loc[index, "Longitude"] = float(row[point_geometry_field].lstrip('POINT (').rstrip(')').split()[0])
            target_spreadsheet.loc[index, "Latitude"] = float(row[point_geometry_field].lstrip('POINT (').rstrip(')').split()[1])
    except ValueError:
        print("\n\nEnsure that the values in your point geometry field of row number " + str(index + 2) + " of your csv file are indeed correctly typed\n\n")
        t.sleep(60)
        exit()
    
    longitude_field = 'Longitude'
    latitude_field = 'Latitude'
    
elif coordinate_nature == '2':    
    ## Longitude field input
    if longitude_field == '':
        print("\n\nWe could not automatically determine the name of your longitude field. The existing fields in this table are:")
        for column in target_spreadsheet.columns:
            print("\t " + str(column))
        longitude_field_input = input("\nPlease state the exact name of the longitude field in your csv file (MANDATORY): ")
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
                print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv file.")
                t.sleep(10)
                exit()
    
    ## Latitude field input
    if latitude_field == '':
        print("\n\nWe could not automatically determine the name of your latitude field. The existing fields in this table are:")
        for column in target_spreadsheet.columns:
            print("\t " + str(column))
        latitude_field_input = input("\nPlease state the exact name of the latitude field in your csv file (MANDATORY): ")
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
                print("REMINDER: Ensure that the fieldname provided above is both typed correctly (Font case sensitive) and the field actually exists in your csv file.")
                t.sleep(10)
                exit()

    ### Correct lats and longs field data type
    try:
        for index, row in target_spreadsheet.iterrows():
            target_spreadsheet.loc[index, longitude_field] = float(row[longitude_field])
            target_spreadsheet.loc[index, latitude_field] = float(row[latitude_field])
    except ValueError:
        print("\n\nEnsure that the values in your longitude and latitude fields of row number " + str(index + 2) + " of your csv file are indeed correctly typed. \n\n")
        t.sleep(60)
        exit()


## Target Location Coordinates
### Target Longitude
target_lon_input = input("Please state the exact coordinates in decimal degrees of the central longitude (- for West and + for East) for your new site (MANDATORY): ")
if target_lon_input == "" or target_lon_input == " ":
    print("REMINDER: When running this tool, remember to specify the coordinates of the central longitude for your new site according to request above.")
    t.sleep(10)
    exit()
else:
    target_lon = target_lon_input
    
### Target Latitude
target_lat_input = input("Please state the exact coordinates in decimal degrees of the central latitude (- for South and + for North) for your new site (MANDATORY): ")
if target_lat_input == "" or target_lat_input == " ":
    print("REMINDER: When running this tool, remember to specify the coordinates of the central latitude for your new site according to request above.")
    t.sleep(10)
    exit()
else:
    target_lat = target_lat_input
    
    
## Shrink Stretch Value
shrink_stretch_value_input = input("Please state the desired shrink/stretch value for your coordinates pattern. i.e to apply no shrink or stretch to pattern just enter 1; OR to shrink the pattern by a constant of 2 enter 0.5 (which is 1/constant); OR to stretch the pattern by a constant of 4 enter 4 (MANDATORY): ")
if shrink_stretch_value_input == "" or shrink_stretch_value_input == " ":
    print("REMINDER: When running this tool, remember to specify the Shrink or Stretch Value for your new site according to request above.")
    t.sleep(10)
    exit()
else:
    shrink_stretch_value = shrink_stretch_value_input


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


#--------------------------------------------------STEP 1: Determing the central coordinates of the current site---------------------------------------------
print("\nStep 1: Determing the central coordinates of the current site from your " + target_file_name + " file.")

target_spreadsheet_central_lon = target_spreadsheet[longitude_field].mean()
target_spreadsheet_central_lat = target_spreadsheet[latitude_field].mean()


#--------------------------------------------------STEP 2: Determining the central deviation for each trackpoint---------------------------------------------
print("\nStep 2: Determining the central deviation for each trackpoint.")

target_spreadsheet["lon_central_deviation"] = ''
target_spreadsheet["lat_central_deviation"] = ''


for index, row in target_spreadsheet.iterrows():    
    target_spreadsheet.loc[index, "lon_central_deviation"] = (row[longitude_field] - target_spreadsheet_central_lon) * float(shrink_stretch_value)
    target_spreadsheet.loc[index, "lat_central_deviation"] = (row[latitude_field] - target_spreadsheet_central_lat) * float(shrink_stretch_value)


#--------------------------------------------------STEP 3: Create new coordinates using the central deviation and central coordinates of the new site---------------------------------------------
print("\nStep 3: Create new coordinates using the central deviation and central coordinates of the new site.")

for index, row in target_spreadsheet.iterrows():    
    target_spreadsheet.loc[index, longitude_field] = row["lon_central_deviation"] + float(target_lon)
    target_spreadsheet.loc[index, latitude_field] = row["lat_central_deviation"] + float(target_lat)

if coordinate_nature == '1':
    target_spreadsheet = target_spreadsheet.drop(columns=[point_geometry_field, "lon_central_deviation", "lat_central_deviation"])
elif coordinate_nature == '2':
    target_spreadsheet = target_spreadsheet.drop(columns=["lon_central_deviation", "lat_central_deviation"])
    
output_csv_file_name = target_file[:-4] + "_shifted.csv"
target_spreadsheet.to_csv(output_csv_file_name, index=False)

endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
print("\n\nProcess completed. Please refer to your output files in the directory: " + str(pathlib.Path(target_file).parent.absolute()) + ".")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))