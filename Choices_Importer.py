'''-------------------------------------------------------------------------
Script Name:      Choices Importer
Version:          1.0
Description:      This tool automates the importing of field choices for
                    event types from a choices.csv file.
Created By:       Kusasalethu Sithole
Created Date:     2021-01-14
Last Revised By:  Kusasalethu Sithole
Last Revision:    2021-01-14
-------------------------------------------------------------------------'''

print("\n\nTOOL - Choices Importer")
print("""\nReminder - For this tool to execute successfully, your machine needs:\n\t
      1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t
      2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.\n\t
      3) Your choices.csv file must have been generated already using the er_event_schema_creator.py tool AND checked to ensure there are no special characters or errors.""")

                                                                   
#---------------------------------------Import Libraries----------------------------------------------------------------------
import datetime
import os
import pandas as pd
import pathlib
import requests
import time as t
import uuid


#---------------------------------------Declaring Input Data----------------------------------------------------------------------
## cURL contents
print("""\n\n\n6 Instructions for the FIRST TIME you run this script:
      \n\t 1)From your Google Chrome web browser, please go to the ER site that you want to load your choices into.Then go to the Add choice page.
      \n\t 2) With the Network tab of the Developer Tools open, manually add the FIRST CHOICE in your choices.csv file.
      \n\t 3) In your Network tab of the Developer Tools, find the request call 'add/' and then right click it and Copy as cURL(bash).
      \n\t 4) Paste the copied cURL contents into a text file, and then use this copied content to update the headers dictionary in this python script.
      \n\t 5) Use the copied cURL contents to also update the csrfmiddlewaretoken  and site address values in this python script (you will find this cURL information in the --data-raw element in your cURL text file).
      \n\t 6) NB: Remember to stop this script, and then save this script and then RERUN it again so that your updated headers and values can be used by this script.""")
                                                                   
## Use the copied cURL contents to update the headers dictionary below                                                                   
headers = {
    'authority': 'sabisands.pamdas.org',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'origin': 'https://sabisands.pamdas.org',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://sabisands.pamdas.org/admin/choices/choice/add/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.989508353.1607494565; OptanonAlertBoxClosed=2021-01-29T13:40:46.598Z; csrftoken=3SojWmdzIEKoNbL8XIZ09gtdpvL8dqkIASu2isWjLCMcmFwmu9wkFhWtX0iyBeh4; sessionid=89etb37ust7gp6il9knbs819os16qetp; _gid=GA1.2.1155336314.1613113021; token=3CoI4Tlfb9cKnrc8nYujUjTVdkJHrU; OptanonConsent=isIABGlobal=false&datestamp=Fri+Feb+12+2021+12%3A56%3A05+GMT%2B0200+(South+Africa+Standard+Time)&version=6.12.0&hosts=&consentId=c7b3223c-3aad-4322-8ce0-a5adfa1a21a7&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=ZA%3BGP&AwaitingReconsent=false',
}

## Use the previously copied cURL contents to update the csrfmiddlewaretoken and site address values below (you will find this information in the --data-raw element in the cURL contents)
csrfmiddlewaretoken = 'YJc45qQNcSTLNzjwKsB8ipnWTemLia4IvJiNrwzxfQVzm34KhT8sOqQcrJTbGY14'
site_address = 'https://sabisands.pamdas.org'


## Choice.csv input
csv_file = input("\n\n\nAbsolute path of the target csv file (MANDATORY): ")
if csv_file == "":
    print("REMINDER: When running this tool, remember to specify the absolute path of the target csv file according to request above.")
    t.sleep(10)
    exit()
if not os.path.isfile(csv_file):
    print("REMINDER: Ensure that the absolute path provided above is both typed correctly and the csv file actually exists.")
    t.sleep(10)
    exit()

csv_df = pd.read_csv(csv_file, names = ['field', 'value', 'display', 'ordernum'])   # Load the csv input file


#-----------------------------------------------Preparing the environment---------------------------------------------
os.chdir(pathlib.Path(csv_file).parent.absolute())


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

#--------------------------------------------------STEP: Uploading choices into your chosen ER Site---------------------------------------------
print("\n STEP: Uploading choices into your chosen ER Site.")

for choice_Index, choice_Row in csv_df[1:].iterrows():
    # generating UUID for choice id
    choice_id = str(uuid.uuid4())
    # compiling the data
    data = {
      'csrfmiddlewaretoken': csrfmiddlewaretoken,
      'id': choice_id,
      'initial-id': choice_id,
      'model': 'activity.event',
      'field': choice_Row.field,
      'value': choice_Row.value,
      'display': choice_Row.display,
      'icon': '',
      'ordernum': choice_Row.ordernum,
      '_save': 'Save'
    }
    # sending the request
    response = requests.post(site_address + '/admin/choices/choice/add/', headers=headers, data=data)   


endTime = currentSecondsTime()

# --------------------------- End of Process ---------------------------
print("\n\n Choices uploaded.")
showPyMessage(" -- Process took {}. ".format(timeTaken(startTime, endTime)))
