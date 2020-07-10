"""---------------------------------------------------------------------------
Script Name:      Convert shapefiles in directory into geojson
Version:          1.1
Description:      This tool automates the conversion of multiple shapefiles
                  within a folder into geojson format and - if the associated 
                  .prj files exist - reprojects the the layers into EPSG4236.
Created By:       Tebogo Kgongwana
Created Date:     2020-06-18
Last Revised By:  Tebogo Kgongwana
Last Revision:    2020-06-25
 ---------------------------------------------------------------------------"""

#Importing Modules
import geopandas
import time
import os

print("TOOL - Shapefile to GeoJSON Converter")
print("Reminder - For this tool to execute successfully, your machine needs:\n\t 1) the anaconda package and have its bin directory mapped in the machines 'path' system environment variable.\n\t 2) The geopandas library installed using your anaconda package.")

#---------------------------Declaring Data Paths------------------
shp = input("Absolute path of the folder with the shapefiles: ")
if shp == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the folder which has the shapefiles according to request above.")
    time.sleep(10) #delay for 10 seconds
    exit()
os.chdir(shp)
destination = input("Absolute path of the directory that will receive the geojson data: ")
if destination == "":
    print("REMINDER: When running this tool, remember to specify the absolute path to the directory for the output geojson files according to request above.")
    time.sleep(10) #delay for 10 seconds
    exit()

# ---------------------------Converting the shapefiles into geojson, and where applicable, reprojecting into EPSG4326---------------------------
print("Converting the shapefiles into geojson, and where applicable, reprojecting into EPSG4326")
for filename in os.listdir(shp):
    if filename.endswith(".shp"):
        myshpfile = geopandas.read_file(filename)
        myshpfile.crs
        projfile = filename.rstrip("shp") + "prj" 
        crs = myshpfile.crs
        for file in os.listdir(shp):
            if file == projfile and crs != {'init': 'epsg:4236'}:
                myshpfile.to_crs({'init': 'epsg:4236'}) #Reprojecting into EPSG4236
        myshpfile.to_file(destination + '/' + filename.rstrip("shp") + "geojson", driver='GeoJSON')

# --------------------------- End of Process ---------------------------
print("End of Process")


