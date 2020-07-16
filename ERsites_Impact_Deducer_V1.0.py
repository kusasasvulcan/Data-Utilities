'''-------------------------------------------------------------------------
Script Name:      ER Sites Impact Deducer
Version:          1.0
Description:      This tool automates deduces the IUCN endangered/vulnerable
                    animal species per ER Site.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-06
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-07-07
-------------------------------------------------------------------------'''

#Import Libraries
import time
import datetime
import geopandas as gpd
import os
import pathlib
from copy import deepcopy
import numpy as np
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool

print("TOOL - ER Sites Impact Deducer")
print("Reminder - For this tool to execute successfully, your machine needs:\n\t 1) the anaconda package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The geopandas library installed using your anaconda package.")

#---------------------------Declaring Data Paths------------------
## ER Sites Layer input
er_sites_shp = input("Absolute path of the ER sites shapefile: ")
if er_sites_shp == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the ER Sites shapefile according to request above.")
    time.sleep(10)
    exit()
if not os.path.isfile(er_sites_shp):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    time.sleep(10)
    exit()
er_sites_shp_gdf = gpd.read_file(er_sites_shp)
er_sites_shp_name = os.path.basename(er_sites_shp)

## Animals Layer input
animal_shp = input("Absolute path of the animals shapefile: ")
if animal_shp == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the animals shapefile according to request above.")
    time.sleep(10)
    exit()
if not os.path.isfile(animal_shp):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    time.sleep(10)
    exit()
animal_shp_gdf = gpd.read_file(animal_shp)
animal_shp_name = os.path.basename(animal_shp)
print("\nThe fields in this animals layer:")
for field in animal_shp_gdf.columns:
    print("\t" + str(field))

## Target filter field input
target_field = input("Exact name of the field with the values for the filter check and application in the animals shapefile: ")
if target_field == "":
    print("REMINDER: When running this tool, remember to specify the name of the field with the values to potentially filter according to request above.")
    time.sleep(10)
    exit()
field_no = len(animal_shp_gdf.columns)
iter_no = 0
for field in animal_shp_gdf.columns:
    if field == target_field:
        break 
    elif  iter_no < field_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the field provided above is both typed correctly (Font case sensitive) and the field actually exists in the target layer.")
        time.sleep(10)
        exit()

#---------------------------Preparing the environment------------------
os.chdir(pathlib.Path(animal_shp).parent.absolute())


#---------------------------Defining common custom functions------------------
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

def multithreading(table, func):
	cores=mp.cpu_count()
	df_split = np.array_split(table, cores, axis=0)

	pool = Pool(cores)
	np.vstack(pool.map(func, df_split))

	#close down the pool and join
	pool.close()
	pool.join()
	pool.clear()


startTime = currentSecondsTime()

# ---------------------------STEP 1: Clipping the animals layer by the er sites layer---------------------------
print("\nStep 1: Clipping the " + animal_shp_name + " layer by the " + er_sites_shp_name + " layer.")
animal_shp_gdf = animal_shp_gdf.to_crs(epsg=3857)
er_sites_shp_gdf = er_sites_shp_gdf.to_crs(epsg=3857)

def buffering():
    global animal_shp_gdf
    animal_shp_gdf = animal_shp_gdf.buffer(0.0001)   #Compensate for invalid geometries

multithreading(animal_shp_gdf, buffering())

clipped_animal_shp_gdf = gpd.clip(animal_shp_gdf, er_sites_shp_gdf) #Clip

clean_indices = []          #Indices with non-polygons
for index, row in clipped_animal_shp_gdf.iterrows():
    if row["geometry"] != "MULTIPOLYGON" and row["geometry"] != "POLYGON":
        clean_indices += '[' + str(index) + ']'
if clean_indices != []:
    clipped_animal_shp_gdf.drop(clean_indices)
    
new_filename = animal_shp_name[:-4] + "_clipped.shp"
clipped_animal_shp_gdf.to_file(new_filename)
print("\t -----Successfully exported the " + new_filename + " shapefile.")
    

# ---------------------------STEP 2: Creating a species list from the target field---------------------------
print("\nStep 2: Creating a species list from the target " + target_field + " field of the " + animal_shp_name + " target layer.")
unique_field_values = ["9%3&4@67!"] #used very random initial list value
for cell_value in clipped_animal_shp_gdf[target_field]:
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

if unique_no < 1 or unique_no is None:
    print("\nFound no species in the target " + target_field + " field. This script is hereby exiting.")
    time.sleep(15)
    exit()
    
    
# ---------------------------STEP 3: Filtering the layer by the unique target values and exporting output as new layers---------------------------
print("\nStep 3: Filtering the " + animal_shp_name + " target layer by the unique target values and exporting output as new layers.")
for unique_value in unique_field_values:
    unique_value_shp = clipped_animal_shp_gdf[clipped_animal_shp_gdf[target_field] == unique_value]
    new_filename = animal_shp_name[:-4] + "_" + str(unique_value) + ".shp"
    unique_value_shp.to_file(new_filename)
    print("\t -----Successfully exported the " + new_filename + " shapefile.")


# ---------------------------STEP 4: Creating a total animal species count per ER site---------------------------
print("\nStep 4: Creating a total animal species count per ER site.")
impact_per_er_site_gdf = deepcopy(er_sites_shp_gdf)
impact_per_er_site_gdf["tot_count"] = ""
for row_index, row in impact_per_er_site_gdf.iterrows():
    intersection = clipped_animal_shp_gdf[clipped_animal_shp_gdf["geometry"].intersects(row["geometry"])]
    if intersection is not None:
        count = intersection.count()
        impact_per_er_site_gdf["tot_count"][row_index] = count

new_filename = "Impact_per_ER_Site.shp"
impact_per_er_site_gdf.to_file(new_filename)
print("\t -----Successfully exported the " + new_filename + " shapefile.")


endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
showPyMessage(" -- Preprocessing done. Process took {}. ".format(timeTaken(startTime, endTime)))
print("Please refer to your output files in the directory: " + str(pathlib.Path(animal_shp).parent.absolute()) + ".")