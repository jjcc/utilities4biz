from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '15BVwLvI52Ft8fwZR7IEVnLp2v0SdPE45-aDnzVoM6VM' #Tracking everything
RANGE_NAME = 'Projects!A2:D'
'''
Procedure:
Need to use the online API explorer to test the API upon given Spread Sheet ID to get access right.
'''

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        #flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES) #project of GSheetProject, in evlab.inc
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s ' % (row[0], row[1] ))

if __name__ == '__main__':
    main()