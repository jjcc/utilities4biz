import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import dotenv
import os
import re
from BookKeepying import remove_trival_chars, get_sums, generate_keys, collect_keys

dotenv.load_dotenv()

# Get the data directory from the .env file
data_dir = os.getenv("DATA_DIR")

# Get the file name from the .env file
BANK_SHEET= os.getenv("BKS")
VISA_SHEET = os.getenv("VSS")

def authenticate_and_connect():
    # Path to your service account JSON key file
    SERVICE_ACCOUNT_FILE = "meta/credential.json"

    # Define the scope
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    # Authenticate
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # Connect to Google Sheets
    gc = gspread.authorize(credentials)
    # Open the spreadsheet by key
    spreadsheet = gc.open_by_key("1ErAPjFEuGAxFKT2FEPCYgpSewEnNLvIgpOUl8loNBfs")  # Replace with your spreadsheet's key

    return spreadsheet

spreadsheet = authenticate_and_connect()

# Select a worksheet by title or index
worksheet = spreadsheet.worksheet(VISA_SHEET)  


rows = worksheet.get_all_records()
# put into a dataframe
df = pd.DataFrame(rows)

for idx, row in enumerate(rows):
    description = row["Description"]
    row_no = idx + 2 # header occupies 1, base 0 instead of 1. So the  add 2
    spend = row["Out"]
    if spend == "":
        continue
    print(f"idx {idx}, RowNo {row_no}: {description}, spend: {spend}")
    #print(row)
    if idx > 100:
        break

# Write data
#worksheet.update('A1', 'Hello, Google Sheets!')  # Update cell A1 with new data
