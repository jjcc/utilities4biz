from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
store = file.Storage('store.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])
for f in files:
    print(f['name'], f['mimeType'])

#OAuth key
#client_secret_594416948416-18tmu5uhjeirnhnncmjn8kr8iphvqqi1.apps.googleusercontent.com.json

#service account key
#API Project-17afd67e179b.json


#[<Spreadsheet 'HelloGSheet' id:1k6pHfz85mD1EA0xWqfb4doedaW7vmXlgA4k01vNxvUE>]