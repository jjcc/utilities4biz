from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "meta/credential.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_gs_files(service_account_file, scopes):
    """
    Retrieve a list of Google Drive files accessible by the service account.
    
    Args:
        service_account_file (str): Path to the service account credentials file
        scopes (list): List of Google API scopes required for access
        
    Returns:
        list: List of file dictionaries containing file metadata
    """
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)

    # List the first 10 files the service account has access to
    results = service.files().list(pageSize=10).execute()
    returned_files = results.get('files', [])
    return returned_files


files = get_gs_files(SERVICE_ACCOUNT_FILE, SCOPES)

print("Accessible files:")
for file in files:
    print(f"Name: {file['name']}, ID: {file['id']}")
