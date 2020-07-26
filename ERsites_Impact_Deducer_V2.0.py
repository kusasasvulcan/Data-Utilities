'''-------------------------------------------------------------------------
Script Name:      ER Sites Impact Deducer
Version:          2.0
Description:      This tool automates deduces the IUCN endangered animal
                    species per ER Site.
Created By:       Kusasalethu Sithole
Created Date:     2020-07-06
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-07-26
-------------------------------------------------------------------------'''

#Import Libraries
import datetime
import geopandas as gpd
import os
import psycopg2
import time

print("\n\nTOOL - ER Sites Impact Deducer")
print("\nReminder - For this tool to execute successfully, your machine needs:\n\t 1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The geopandas library installed using your pip package.")

#---------------------------Declaring Data Paths------------------
## Working Directory
working_directory = input("\nAbsolute path of the working directory: ")
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
    
pg_con = psycopg2.connect(host = pghost, database = pgdatabase, port = pgport, user = pguser, password = pgpassword)


#---------------------------Preparing the environment------------------
os.chdir(working_directory)


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


startTime = currentSecondsTime()

# ---------------------------STEP 1: Clipping the IUCN's Terrestrial Mammals layer by the ER Sites layer---------------------------
print("\nStep 1: Clipping the IUCN's Terrestrial Mammals layer by the ER Sites layer.")
S1_startTime = currentSecondsTime()

sql_1 = "SELECT a.name er_site, b.binomial species, a.geom geom FROM er_sites a, terrestrial_mammals b WHERE st_intersects(a.geom, b.geom);"
sites_mammals = gpd.GeoDataFrame.from_postgis(sql_1, pg_con, geom_col='geom' )
sites_mammals.to_file(".\ER_Sites_IUCN_Terrestrial_Mammals.shp")

S1_endTime = currentSecondsTime()
showPyMessage("\n -- Step 1 completed successfully. Step took {}. ".format(timeTaken(S1_startTime, S1_endTime)))

# ---------------------------STEP 2: Filtering only the Critically Endangered Terrestrial Mammals that overlap the ER Sites---------------------------
print("\nStep 2: Filtering only the Critically Endangered Terrestrial Mammals that overlap the ER Sites.")
S2_startTime = currentSecondsTime()

sql_2 = "SELECT a.name er_site, b.binomial species, CASE WHEN b.category = 'CR' THEN 'Critically Endangered' ELSE '' END status, a.geom geom FROM er_sites a, terrestrial_mammals b WHERE st_intersects(a.geom, b.geom) AND UPPER(b.category)='CR';"
filtered_sites_mammals = gpd.GeoDataFrame.from_postgis(sql_2, pg_con, geom_col='geom' )
filtered_sites_mammals.to_file(".\Critically_Endangered_ER_Sites_IUCN_Terrestrial_Mammals.shp")

S2_endTime = currentSecondsTime()
showPyMessage("\n -- Step 2 completed successfully. Step took {}. ".format(timeTaken(S2_startTime, S2_endTime)))
    
    
# ---------------------------STEP 3: Summing the filtered Critically Endangered Terrestrial Mammals per ER Site---------------------------
print("\nStep 3: Summing the filtered Critically Endangered Terrestrial Mammals per ER Site.")
S3_startTime = currentSecondsTime()

sql_3 = "WITH site_CR_T_Mammals AS (SELECT a.name er_site, b.binomial species, CASE WHEN b.category = 'CR' THEN 'Critically Endangered' ELSE '' END status, a.geom geom FROM er_sites a, terrestrial_mammals b WHERE st_intersects(a.geom, b.geom) AND UPPER(b.category)='CR') SELECT MIN(er_site) er_site, MIN(status) status, COUNT(er_site) IUCN_Impact, MIN(geom) geom FROM site_CR_T_Mammals GROUP BY er_site;"
summed_filtered_sites_mammals = gpd.GeoDataFrame.from_postgis(sql_3, pg_con, geom_col='geom' )
summed_filtered_sites_mammals["Species"] = ""

for x_index, x_row in summed_filtered_sites_mammals.iterrows():
        site = x_row["er_site"]
        species_list = []
        target_records = filtered_sites_mammals[filtered_sites_mammals["er_site"] == site]
        for y_index, y_row in target_records.iterrows():
            species_list.append(y_row["species"])
        species_no = len(species_list)
        species = species_list[0]
        itr = 1
        while itr < species_no:
            species = species + ";" + species_list[itr]
            itr += 1
        summed_filtered_sites_mammals.loc[x_index, "Species"] = species

summed_filtered_sites_mammals.to_file(".\ER_Sites_IUCN_Impact.shp")

S3_endTime = currentSecondsTime()
showPyMessage("\n -- Step 3 completed successfully. Step took {}. ".format(timeTaken(S3_startTime, S3_endTime)))


endTime = currentSecondsTime()

# --------------------------- End of Process ---------------------------
showPyMessage("\n\nProcessing done. Process took {}. ".format(timeTaken(startTime, endTime)))
print("Please refer to your output files in your working directory: " + str(working_directory) + ".")
