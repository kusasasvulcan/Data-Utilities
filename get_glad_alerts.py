"""--------------------------------------------------------------------------------------------------
Script Name:      Get GLAD Alert Counts
Version:          1.0
Description:      This tool fetches GLAD Alert counts per time period.
Created By:       Dennis Schneider 
Created Date:     2020-99-99
Last Revised By:  Kusasalethu Sithole
Last Revision:    2020-09-17
---------------------------------------------------------------------------------------------------"""

print("\n\nTOOL - Get GLAD Alert Counts")


#---------------------------------------Importing Libraries------------------------------------------
from datetime import date, timedelta
import json
import requests
import time


#---------------------------------------Declaring User Inputs-----------------------------------------
## GLAD GEOSTORE ID
GLAD_GEOSTORE_ID = input("\nPlease provide a valid GLAD GEOSTORE ID, i.e. e890132370e54921c987417cddfd972f (MANDATORY): ")
if GLAD_GEOSTORE_ID == "" or GLAD_GEOSTORE_ID == " ":
    print("REMINDER: When running this tool, remember to specify the GLAD GEOSTORE ID according to request above.")
    time.sleep(15)
    exit()

## Start Date
start_date = input("\nPlease provide a start date for the GLAD Alert period according to format yyyy-mm-dd, i.e. 2020-06-15 (OPTIONAL). If you are not sure, leave blank: ")
if start_date == "" or start_date == " ":
    pass
elif len(start_date) != 10 or start_date[4] != '-' or start_date[7] != '-':
    print("REMINDER: Since you have chosen to provide the start date, remember to specify the start date using the required format according to request above.")
    time.sleep(15)
    exit()

## Confirmed_Only Status
confirmed_only = input("\nPlease state - True or False - to choose whether the query should fetch just the confirmed_only reports (OPTIONAL). If you are not sure, leave blank: ")
if confirmed_only == "" or confirmed_only == " ":
    confirmed_only = 'False' #The default status
    pass
elif confirmed_only.lower() != 'false' and confirmed_only.lower() != 'true':
    print("REMINDER: Since you have chosen to provide the Confirmed_Only status, your choice has to be either True or False according to request above.")
    time.sleep(15)
    exit()

if confirmed_only.lower() == 'false':
    confirmed_only = False
elif confirmed_only.lower() == 'true':
    confirmed_only = True


#--------------------------------------Defining custom function---------------------------------------
def get_time_periods_list(start_date, end_date, step=7):
    time_periods = []
    while start_date < end_date:
        period_end = start_date + timedelta(step)
        start_str = date.strftime(start_date, '%Y-%m-%d')
        period_end_str = date.strftime(period_end, '%Y-%m-%d')
        
        time_periods.append(f'{start_str} to {period_end_str}')
        start_date = period_end
    
    return time_periods

def fetch_glad_for_geostore(geostore, start_date, end_date, confirmed_only=False, step=7):
    true_total = 0
    true_num_alerts = []
    all_total = 0
    all_num_alerts = []
    while start_date < end_date:
        period_end = start_date + timedelta(step)
        start_str = date.strftime(start_date, '%Y-%m-%d')
        period_end_str = date.strftime(period_end, '%Y-%m-%d')

        if confirmed_only == True:
            download_url = f'https://production-api.globalforestwatch.org/glad-alerts/download/?period={start_str},{period_end_str}&gladConfirmOnly={confirmed_only}&aggregate_values=False&aggregate_by=False&geostore={geostore}&format=json'
            rsp = requests.get(download_url)        
            alert_data = json.loads(rsp.text).get('data', [])
            cnt = len(alert_data)
            true_total += cnt
            true_num_alerts.append(cnt)
                # print(f'{start_str} to {period_end_str} {cnt} total {true_total}')
                # print(alert_data)
                # print(download_url)
        else:
            download_url = f'https://production-api.globalforestwatch.org/glad-alerts/download/?period={start_str},{period_end_str}&gladConfirmOnly=True&aggregate_values=False&aggregate_by=False&geostore={geostore}&format=json'
            rsp = requests.get(download_url)        
            alert_data = json.loads(rsp.text).get('data', [])
            cnt = len(alert_data)
            true_total += cnt
            true_num_alerts.append(cnt)
                # print(f'{start_str} to {period_end_str} {cnt} total {true_total}')
                # print(alert_data)
                # print(download_url)
                
            download_url = f'https://production-api.globalforestwatch.org/glad-alerts/download/?period={start_str},{period_end_str}&gladConfirmOnly={confirmed_only}&aggregate_values=False&aggregate_by=False&geostore={geostore}&format=json'
            rsp = requests.get(download_url)        
            alert_data = json.loads(rsp.text).get('data', [])
            cnt = len(alert_data)
            all_total += cnt
            all_num_alerts.append(cnt)
                # print(f'{start_str} to {period_end_str} {cnt} total {all_total}')
                # print(alert_data)
                # print(download_url)

        start_date = period_end
    
    if confirmed_only == True:
        return true_num_alerts
    else:
        return true_num_alerts, all_num_alerts


#--------------------------------Getting the GLAD Alert Counts--------------------------------------
today = date.today()
if start_date == "" or start_date == " ":
    start_date = date.today() - timedelta(weeks=6)
else:
    start_date = date.fromisoformat(start_date)
time_periods = get_time_periods_list(start_date, today)
step=10

if confirmed_only == True:
    print(f"\n\nGetting alert counts for period {start_date} to {today}, using confirmed_only: {confirmed_only} and step: {step}.")
    print("\n(Time period, Only Confirmed Count) ..........processing.......")
    true_preylang_glad_alert_counts = fetch_glad_for_geostore(GLAD_GEOSTORE_ID, start_date, today, confirmed_only=confirmed_only, step=step)
    
    for item in zip(time_periods, true_preylang_glad_alert_counts):
        print(item)   
else:
    print(f"\n\nGetting alert counts for period {start_date} to {today}, using confirmed_only: {confirmed_only} and step: {step}.")
    print("\n(Time period, Only Confirmed Count, Combined Count) ..........processing.......")
    true_preylang_glad_alert_counts,  all_preylang_glad_alert_counts= fetch_glad_for_geostore(GLAD_GEOSTORE_ID, start_date, today, confirmed_only=confirmed_only, step=step)
    
    for item in zip(time_periods, true_preylang_glad_alert_counts, all_preylang_glad_alert_counts):
        print(item)
        

# ---------------------------End of Process ---------------------------
print("\n\nProcess Complete.")        