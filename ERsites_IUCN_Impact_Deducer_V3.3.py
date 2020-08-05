'''---------------------------------------------------------------------------------
Script Name:      ER Sites IUCN Impact Deducer
Version:          3.3
Description:      This tool automates the deduction of the IUCN Animal species per
                    ER Site (hence the ER Sites IUCN Impact).
Created By:       Kusasalethu Sithole
Created Date:     2020-07-06
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-08-05
---------------------------------------------------------------------------------'''


print("\n\nTOOL - ER Sites Impact Deducer")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The geopandas, psycopg2 libraries installed using your pip package.")


#Import Libraries
import datetime
import geopandas as gpd
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import time


#-----------------------------------Declaring Data Paths--------------------------
## Working Directory
working_directory = input("\nAbsolute path of the working directory which will receive the output files: ")
if working_directory == "":
    print("\nREMINDER: When running this tool, remember to specify the absolute path of the working directory according to request above.")
    time.sleep(10)
    exit()
if not os.path.isdir(working_directory):
    print("\nREMINDER: Ensure that the absolute path provided above is both typed correctly and the layer file actually exists.")
    time.sleep(10)
    exit()

## Postgres
pghost = input("\nPostgres Host Address: ")
pgport = input("Postgres Database Server Port: ")
pgdatabase = input("Postgres Database Name: ")
pguser = input("Postgres Username: ")
pgpassword = input("Postgres User Password: ")
    
postgres_engine = create_engine('postgresql://' + pguser + ':' + pgpassword + '@' + pghost + ':' + pgport + '/' + pgdatabase)
pg_con = psycopg2.connect(host = pghost, database = pgdatabase, port = pgport, user = pguser, password = pgpassword)

## State target IUCN category
sql_iucn_categories = "SELECT DISTINCT(category) status FROM iucn_animals;"
categories = pd.read_sql_query(sql_iucn_categories,con=postgres_engine)

print("\n\nThe existing IUCN categories are:")
for row in categories["status"]:
    print("\t " + str(row))

target_category_key = input("Please state the exact name of your IUCN category of interest (MANDATORY): ")
if target_category_key == "" or target_category_key == " ":
    print("REMINDER: When running this tool, remember to specify the name of your IUCN category of interest according to request above.")
    time.sleep(10)
    exit()

row_no = len(categories)
iter_no = 0
for row in categories["status"]:
    if row == target_category_key:
        break 
    elif  iter_no < row_no - 1:
        iter_no += 1
        continue
    else:
        print("REMINDER: Ensure that the category name provided above is both typed correctly (Font case sensitive) and the category actually exists in the IUCN layer.")
        time.sleep(10)
        exit()

category_names = {"LC":"Least Concern",
                 "EX":"Extinct",
                 "CR":"Critically Endangered",
                 "EN":"Endangered",
                 "VU":"Vulnerable",
                 "DD":"Data Deficient",
                 "EW":"Extinct in the Wild",
                 "NT":"Near Threatened",
                 "LR/cd":"LR/cd",
                 "LR/lc":"LR/lc"}

target_category_name = category_names[target_category_key]


#-----------------------------------Preparing the environment------------------------------
os.chdir(working_directory)


#-----------------------------------Defining common custom functions-----------------------
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


# ---------------------------STEP 1: Filtering only the Animals of the user target category that overlap the ER Sites---------------------------
print("\nStep 1: Filtering only the {} Animals that overlap the ER Sites.".format(target_category_name))
S1_startTime = currentSecondsTime()

sql_1 = "SELECT a.name er_site, b.binomial species, CASE WHEN b.category = '{0}' THEN '{1}' ELSE '' END status, ST_MakeValid(a.geom) geom FROM er_sites a, iucn_animals b WHERE st_intersects(ST_MakeValid(a.geom), ST_MakeValid(a.geom)) AND UPPER(b.category)='{0}';".format(target_category_key, target_category_name)
filtered_sites_animals = gpd.GeoDataFrame.from_postgis(sql_1, pg_con, geom_col='geom' )
filtered_sites_animals.to_file(".\{}_ER_Sites_IUCN_Animals.shp".format(target_category_name))

S1_endTime = currentSecondsTime()
showPyMessage("\n -- Step 1 completed successfully. Step took {}. ".format(timeTaken(S1_startTime, S1_endTime)))
    

# ---------------------------STEP 2: Summing the filtered Animals of the user target category per ER Site---------------------------
print("\nStep 2: Summing the filtered {} Animals per ER Site.".format(target_category_name))
S2_startTime = currentSecondsTime()

sql_2 = "WITH site_CR_T_Animals AS (SELECT a.name er_site, b.binomial species, CASE WHEN b.category = '{0}' THEN '{1}' ELSE '' END status, ST_MakeValid(a.geom) geom FROM er_sites a, iucn_animals b WHERE st_intersects(ST_MakeValid(a.geom), ST_MakeValid(a.geom)) AND UPPER(b.category)='{0}') SELECT MIN(er_site) er_site, MIN(status) status, COUNT(er_site) IUCN_Impact, string_agg(species, '; ') Species_List, MIN(geom) geom FROM site_CR_T_Animals current GROUP BY er_site;".format(target_category_key, target_category_name)
summed_filtered_sites_animals = gpd.GeoDataFrame.from_postgis(sql_2, pg_con, geom_col='geom' )
summed_filtered_sites_animals.to_file(".\ER_Sites_IUCN_Impact.shp")

S2_endTime = currentSecondsTime()
showPyMessage("\n -- Step 2 completed successfully. Step took {}. ".format(timeTaken(S2_startTime, S2_endTime)))


endTime = currentSecondsTime()


# --------------------------- End of Process ---------------------------
showPyMessage("\n\nProcessing done. Process took {}. ".format(timeTaken(startTime, endTime)))
print("Please refer to your output files in your working directory: " + str(working_directory) + ".")
