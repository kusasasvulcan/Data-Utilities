@echo off
rem -------------------------------------------------------------------------------------------
rem Script Name:      Shapefile To EPSG4326 and GeoJSON Convertor
rem Version:          1.0
rem Description:      This tool automates the conversion of multiple shapefiles within a folder 
rem		      into geojson format - reprojection them into EPSG4326 in the process.
rem Created By:       Kusasalethu Sithole
rem Date:             2020-06-08
rem Last Revised By:  Kusasalethu Sithole
rem Last Revision:    2020-06-08
rem -------------------------------------------------------------------------------------------

@echo TOOL - Shapefile To EPSG4326 and GeoJSON Convertor
@echo ~
@echo Reminder: For this tool to execute successfully, your machine needs:
@echo          1) the gdal library (https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) and have its bin directory mapped in the machines 'path'system environment variable.
@echo ~    

@echo ---------------------------Declaring data paths------------------
set /P shp="Absolute path of the folder with the shapefiles: "
if %shp%.==. GOTO No1
cd /d %shp%
set /P destination="Absolute path of the folder that will receive the geojson data: "
if %destination%.==. GOTO No2

@echo ~ 

@echo ---------------------------Converting the shapefiles into geojson---------------------------
for %%l in ("*.shp") do (
	IF EXIST "%%~nl.prj" (ogr2ogr -t_srs EPSG:4326 "%destination%\%%~nl.geojson" "%%~fl")
	IF NOT EXIST "%%~nl.prj" (ogr2ogr "%destination%\%%~nl.geojson" "%%~fl")
)
@echo ~ 

@echo --------------------------- End of Process ---------------------------

@echo ~
GOTO End1

:No1  
  ECHO ~~~~~ REMINDER: When running this tool, remember to specify the absolute path of the folder which has the shapefiles according to request above.
GOTO End1

:No2  
  ECHO ~~~~~ REMINDER: When running this tool, remember to specify the absolute path to the directory for the output geojson files according to request above.
GOTO End1

:End1
PAUSE