import pandas as pd
import numpy as np
import dotenv
import os
import re

# Load .env file
dotenv.load_dotenv()

# Get the data directory from the .env file
data_dir = os.getenv("DATA_DIR")

# Get the file name from the .env file
stmts_fn = os.getenv("BANK_STMTS")
bank_sheet = os.getenv("BKS")
visa_sheet = os.getenv("VSS")
start_row = 33
end_row = 193

def parse_xlsx(data_dir, visa_fn, sheet_name, func = None):
    '''
    Parse the xlsx file and return the dataframe
    available functions: get_keys, get_sums, get_all
    '''
    vxls_file = pd.ExcelFile(f"{data_dir}/{visa_fn}")
    #vxls_file = pd.read_excel(f"{data_dir}/{visa_fn}")

    print(vxls_file.sheet_names)

    df0 = vxls_file.parse(sheet_name)
    df = df0.fillna("")
    cols = df.columns
    print(cols)

    if func == "get_keys":
        df = generate_keys(sheet_name, df)
        return

    elif func == "get_sums":
        df = get_sums(sheet_name, df)
        print(df.head())
    
    elif func == "get_all":
        key_fn = f"{sheet_name}_keys.txt"
        keys = open(key_fn).read().splitlines()

        df = generate_keys(sheet_name, df)
        df = get_sums(sheet_name, df)
        print(df.head())
    elif func == "fill_cat":
        fill_cat(sheet_name, df)
    else:
        print("Invalid function")

def fill_cat(sheet_name, df):
    '''
    Fill the category column'''
    dfkeys = pd.read_csv(f"{sheet_name}_keys.csv")
    dict_keys = dfkeys.set_index("Key").T.to_dict('dict')
    lmda_trans = lambda x: dict_keys[x]["Cat"] if x in dict_keys else "Unknown"
    df["Res2"] = df["Description"].apply(remove_trival_chars)
    df["Code"] = df["Res2"].apply(lmda_trans)# if df["Code"].empty else df["Code"])
    df.to_csv(f"{sheet_name}_catfilled1.csv")

def get_sums(sheet_name, df):
    df = df.iloc[start_row:end_row]    
    df["Outf"] = df["Out"].apply(lambda x: float(x) if x != "" else 0)
    dfgreg = df["Outf"].groupby(df["Code"])
    res = dfgreg.sum()
    res.to_csv(f"{sheet_name}_cat_sum.csv")
    return df

def generate_keys(sheet_name, df):
    df["Description"] = df["Description"].apply(remove_trival_chars)

    desc_col = df["Description"]
    desc_vals0 = list(desc_col.values)
    desc_vals = [ x for x in desc_vals0 if "PAYMENT" not in x ]
    desc_set = set(desc_vals)
    open(f"{sheet_name}_keys.txt", "w").write("\n".join(desc_set))
    return df



def remove_trival_chars(s):
    '''
    remove the trailing chars like #, *, etc.
    for example, "BOSTON PIZZA # 432" -> "BOSTON PIZZA"
    '''
    m1 = re.search(r'\s*[#|*]', s) 
    if m1:
        idx = m1.start()
        s = s[:idx]
    return s


if __name__ == "__main__":
    #parse_xlsx(data_dir, stmts_fn, bank_sheet, func="get_all")
    #parse_xlsx(data_dir, stmts_fn, visa_sheet, func="get_keys")
    parse_xlsx(data_dir, stmts_fn, visa_sheet)