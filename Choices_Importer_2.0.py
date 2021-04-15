'''-------------------------------------------------------------------------
Script Name:      Choices Importer
Version:          2.0
Description:      This tool automates the importing of field choices for
                    event types from a choices.csv file.
Created By:       Kusasalethu Sithole
Created Date:     2021-04-15
Last Revised By:  Kusasalethu Sithole
Last Revision:    2021-04-15
-------------------------------------------------------------------------'''

print("\n\nTOOL - Choices Importer")
print("""\nReminder - For this tool to execute successfully, your machine needs:\n\t
      1) the pip package and have its bin directory mapped in the machines 'path' system environment variable.\n\t
      2) The pandas library is installed using your pip package (i.e. from your terminal run 'pip install pandas'.\n\t
      3) Your choices.csv file must have been generated already using the er_event_schema_creator.py tool.\n\t
      4) You must check your choices.csv file to ensure there are no special characters or errors.\n\t
      5) Your choices file must be placed in the same directory/folder as this script.""")

                                                                   
#---------------------------------------Import Libraries----------------------------------------------------------------------
import json, requests, pandas as pd, time


#---------------------------------------Defining variables----------------------------------------------------------------------
# User-define inputs
ER_site_url_name = 'easterisland'     ## Just the name part of the ER site URL (https://easterisland.pamdas.org/)
auth_token = '2cw697Qb-F066-4dB8-a669-c63666639gff'
csv_file = './choices.csv'

choices_csv = pd.read_csv(csv_file, header=None)


# Headers
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': ('Bearer ' + auth_token)
}


problem_rows_table = pd.DataFrame()

#---------------------------------------Importing the Choices----------------------------------------------------------------------
print("\n\n UPLOADING: Importing your choices into your {} ER Site.".format(ER_site_url_name))

for index, row in choices_csv.iterrows():
    # Auto-defined inputs
    field_value = row[0]
    choice_value = row[1]
    choice_discplay = row[2]
    ordernum = row[3]
    
    # Sending the post requests
    data_dict = { "model": "activity.event", "field": field_value, "value": choice_value, "display": choice_discplay, "ordernum": ordernum}
    data_str  = json.dumps(data_dict).replace ('}', ', "is_active": true }')
    
    response = requests.post('https://{}.pamdas.org/api/v1.0/choices/'.format(ER_site_url_name), headers=headers, data=data_str)
    row_array = [row[0],row[1],row[2],row[3]]
    if response.status_code != 201:
        print("\n\n\n WARNING: Request returned the http code {0} whilst sending row: {1}. Please check your user-defined inputs in this script and/or your choices.csv file\n\n\n".format(str(response.status_code), str(row_array)))
        time.sleep((5))
        problem_rows_table = problem_rows_table.append([[response.status_code] + row_array])
    else:
        print("Imported:", str(row_array))


# --------------------------- End of Process ---------------------------
if problem_rows_table.size == 0:
    print("\nPROCESS COMPLETED: Choices imported successfully.\n\n\n")
else:
    problem_rows_table.to_csv('./POTENTIALLY_Problematic_ChoiceRows.csv', index=False)
    print("\nWARNING: There might have been some issues with some choice(s) during the execution of this import process. Please refer to the POTENTIALLY_Problematic_ChoiceRows.csv file in this script's directory/folder.\n\n\n")