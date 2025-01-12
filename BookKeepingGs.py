import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import dotenv
import os
import re
from BookKeepying import remove_trival_chars, get_sums, generate_keys, collect_keys,manage_keys
'''
1. Authenticate and connect to Google Sheets, get data
2. Generate keys

'''
dotenv.load_dotenv()

fiscal_year = os.getenv("FISCAL_YEAR")
file_prefix = f"meta/{fiscal_year}_"
# Get the data directory from the .env file
data_dir = os.getenv("DATA_DIR")

# Get the file name from the .env file
BANK_SHEET= os.getenv("BKS")
VISA_SHEET = os.getenv("VSS")

current_sheet = VISA_SHEET
max_rows = 300

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

def generate_keys_gs(sheet_name:str, df:pd.DataFrame, end_row) :
    '''
    Prepare the keys for categorization
    '''
    start_row = 2
    df = df.iloc[start_row:end_row]    
    df["Description"] = df["Description"].apply(remove_trival_chars)

    desc_col = df["Description"]
    desc_vals0 = list(desc_col.values)
    desc_vals = [ x for x in desc_vals0 if "PAYMENT" not in x ]
    desc_set = set(desc_vals)
    open(f"{file_prefix}_{sheet_name}_keys.txt", "w").write("\n".join(desc_set))
    return df, desc_set

def update_sheet(sheet, rows, dict_keys):
    '''
    update the sheet with the category
    '''
    cat_list = []
    row_start = 2
    for idx, row in enumerate(rows):
        row_no = idx + 2 # header occupies 1, base 0 instead of 1. So the  add 2
        spend = row["Out"]
        if spend == "":
            cat_list.append([""])
            continue
        exclude = row["Exclude"] if "Exclude" in row else ""
        if exclude == "TRUE":
            cat_list.append([""])
            continue
    #print(f"idx {idx}, RowNo {row_no}: {description}, spend: {spend}")
        desc_brief = remove_trival_chars(row["Description"])
    # get the category
        cat = dict_keys[desc_brief]["Cat"] if desc_brief in dict_keys else "Unknown"
    # update the 
        cat_list.append([cat])


    cell_range = f"J{row_start}:J{row_no}" # for VISA
    sheet.update(cell_range, cat_list)

spreadsheet = authenticate_and_connect()

# Select a worksheet by title or index
worksheet = spreadsheet.worksheet(VISA_SHEET)  


rows = worksheet.get_all_records()
rows = rows[:max_rows]
# put into a dataframe
df = pd.DataFrame(rows)

# 1. generate keys
# df, desc_set = generate_keys_gs(VISA_SHEET, df, 1000)

# 2. manage keys
#manage_keys(current_sheet)


# 3. fill the category
# get the keys
dict_key_df = pd.read_csv(f"{file_prefix}_{current_sheet}_keys.csv")
# convert to dictionary with column 'Key' as the key, 'Cat' as the value
dict_keys = dict_key_df.set_index("Key").T.to_dict('dict')
#update_sheet(worksheet, rows, dict_keys)


# 4. get the sums

# remove rows that the Out column is empty
df = df[df["Out"] != ""]
# removce rows that Exclude column as 'TRUE'
df = df[df["Exclude"] != "TRUE"]

df["Outf"] = df["Out"].apply(lambda x: float(x.replace('$', '').replace(',', '')) if x != "" else 0)
df["Outf"] = df["Outf"].round(2)
dfgreg = df["Outf"].groupby(df["Code"])
res = dfgreg.sum()
res = res.round(2)
res.to_csv(f"{file_prefix}_{current_sheet}_cat_sum.csv")