'''-------------------------------------------------------------------------
Script Name:      Shapefile Field Value Filter & Exporter
Version:          1.0
Description:      This tool automates the identification, and if necessary,
                  the export of layers per field value filter.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-02
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-07-02
-------------------------------------------------------------------------'''

#Import Libraries
import geopandas as gpd
import time
import os
import pathlib

print("TOOL - Shapefile Field Value Filter & Exporter")
print("Reminder - For this tool to execute successfully, your machine needs:\n\t 1) the anaconda package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The geopandas library installed using your anaconda package.")

#---------------------------Declaring Data Paths------------------
target_shp = input("Absolute path of the target shapefile: ")
if target_shp == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target shapefile according to request above.")
    time.sleep(10)
    exit()
if not os.path.isfile(target_shp):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    time.sleep(10)
    exit()
os.chdir(pathlib.Path(target_shp).parent.absolute())
shp = gpd.read_file(target_shp)
shp_name = os.path.basename(target_shp)
print("\nThe fields in this layer:")
for field in shp.columns:
    print("\t" + str(field))

target_field = input("Exact name of the field with the values for the filter check and application: ")
if target_field == "":
    print("REMINDER: When running this tool, remember to specify the name of the field with the values to potentially filter according to request above.")
    time.sleep(10)
    exit()
field_no = len(shp.columns)
iter_no = 0
for field in shp.columns:
    if field == target_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the field provided above is both typed correctly (Font case sensitive) and the field actually exists in the target layer.")
        time.sleep(10)
        exit()
    
# ---------------------------STEP 1: Checking for potential multiple values in the target field---------------------------
print("\nStep 1: Checking for potential multiple values in the target " + target_field + " field of the " + shp_name + " target layer.")
unique_field_values = ["9%3&4@67!"] #used very random initial list value
for cell_value in shp[target_field]:
    unique_no = len(unique_field_values)
    iter_no = 0
    stripped_cell_value = str(cell_value.strip()).title()
    for unique in unique_field_values:
        if unique == stripped_cell_value:
            break
        elif  iter_no + 1 < unique_no:
            iter_no += 1
            continue
        else:
            if unique_field_values == ["9%3&4@67!"]:
                unique_field_values = stripped_cell_value.split(",")
            else:
                unique_field_values += stripped_cell_value.split(",")
            print("\t -----Found " + stripped_cell_value + " as the number " + str(len(unique_field_values)) + " unique value in the target " + target_field + " field.")

if unique_no < 2:
    print("\nOnly found " + str(unique_field_values[0]) + " as the only unique value in the target " + target_field + " field. This script is hereby exiting.")
    time.sleep(15)
    exit()
    
# ---------------------------STEP 2: Filtering the layer by the unique target values and exporting output as new layers---------------------------
print("\nStep 2: Filtering the " + shp_name + " target layer by the unique target values and exporting output as new layers.")
for unique_value in unique_field_values:
    unique_value_shp = shp[shp[target_field] == unique_value]
    new_filename = shp_name[:-4] + "_" + str(unique_value) + ".shp"
    unique_value_shp.to_file(new_filename)
    print("\t -----Successfully exported the " + new_filename + " shapefile.")
    
# --------------------------- End of Process ---------------------------
print("\nEnd of Process. Please refer to your output files in the directory: " + str(pathlib.Path(target_shp).parent.absolute()) + ".")
