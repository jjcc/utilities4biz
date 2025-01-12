import pandas as pd
import numpy as np
import dotenv
import os
import re

#%%

# Load .env file
dotenv.load_dotenv()

# Get the data directory from the .env file
data_dir = os.getenv("DATA_DIR")

# Get the file name from the .env file
stmts_fn = os.getenv("BANK_STMTS")
bank_sheet = os.getenv("BKS")
visa_sheet = os.getenv("VSS")
#start_row = 22 
#end_row =  205
#start_row = 38  # visa start
#end_row = 298   # visa end
start_row = 24  # visa start
end_row = 316   # visa end

fiscal_year = os.getenv("FISCAL_YEAR")
file_prefix = f"meta/{fiscal_year}_"

def parse_xlsx(data_dir, visa_fn, sheet_name, func = None):
    '''
    Parse the xlsx file and return the dataframe
    available functions: get_keys, get_sums, get_all
    '''
    input_file = f"{data_dir}/{visa_fn}"
    vxls_file = pd.ExcelFile(input_file)
    #vxls_file = pd.read_excel(f"{data_dir}/{visa_fn}")

    print(vxls_file.sheet_names)

    df0 = vxls_file.parse(sheet_name)
    df = df0.fillna("")
    cols = df.columns
    print(cols)

    if func == "get_keys":
        df, keyset = generate_keys(sheet_name, df)
        return
    elif func == "collect_keys":
        dict_key_cat = collect_keys(sheet_name, df)
        # write the dict to a csv file
        dfkeys = pd.DataFrame(dict_key_cat.items(), columns=["Key", "Cat"])
        dfkeys.to_csv(f"{file_prefix}_{sheet_name}_exist_keys.csv")

    elif func == "get_sums":
        df = get_sums(sheet_name, df)
        print(df.head())
    
    elif func == "get_all":
        key_fn = f"{file_prefix}_{sheet_name}_keys.txt"
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
    dfkeys = pd.read_csv(f"{file_prefix}_{sheet_name}_keys.csv")
    dict_keys = dfkeys.set_index("Key").T.to_dict('dict')
    lmda_trans = lambda x: dict_keys[x]["Cat"] if x in dict_keys else "Unknown"
    df["Res2"] = df["Description"].apply(remove_trival_chars)
    df["Code"] = df["Res2"].apply(lmda_trans)# if df["Code"].empty else df["Code"])
    df.to_csv(f"{file_prefix}_{sheet_name}_catfilled1.csv")

def get_sums(sheet_name, df):
    '''
    Get the sum of the transactions by category
    '''
    df = df.iloc[start_row:end_row]    
    df = df[df["Flag"] != "Ignore"]
    df["Outf"] = df["Out"].apply(lambda x: float(x) if x != "" else 0)
    df["Outf"] = df["Outf"].round(2)
    dfgreg = df["Outf"].groupby(df["Code"])
    res = dfgreg.sum()
    #res["Outf"] = res["Outf"].round(2)
    res.to_csv(f"{file_prefix}_{sheet_name}_cat_sum.csv")
    return df

def generate_keys(sheet_name:str, df:pd.DataFrame) :
    '''
    Prepare the keys for categorization
    '''
    df = df.iloc[start_row:end_row]    
    df["Description"] = df["Description"].apply(remove_trival_chars)

    desc_col = df["Description"]
    desc_vals0 = list(desc_col.values)
    desc_vals = [ x for x in desc_vals0 if "PAYMENT" not in x ]
    desc_set = set(desc_vals)
    open(f"{file_prefix}_{sheet_name}_keys.txt", "w").write("\n".join(desc_set))
    return df, desc_set

def collect_keys(sheet_name, df):
    '''
    Collect the existing Desc:Code for categorization
    '''
    df, keyset = generate_keys(sheet_name, df)
    dict_key_cat = {}
    for i, row in df.iterrows():
        desc = row["Description"]
        if not isinstance(desc, str):
            continue
        if row["Flag"] == "Ignore":
            continue
        desc_breif = remove_trival_chars(desc) 
        if row['Code'] != "":
            dict_key_cat[desc_breif] = row['Code']
        else:
            dict_key_cat[desc_breif] = "###"
    return dict_key_cat

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


def manage_keys(sheet_name):
    '''
    Manage the keys for categorization
    '''
    key_fn_new = f"{file_prefix}_{sheet_name}_keys.txt"
    keys = open(key_fn_new).read().splitlines()
    dfkeys = pd.DataFrame(keys, columns=["Key"])
    dfkeys["Cat"] = ""

    key_fn_old = f"Visa21-22_keys.csv"
    dfkeys_old = pd.read_csv(key_fn_old)
    for i, row in dfkeys_old.iterrows():
        key = row["Key"]
        cat = row["Cat"]
        dfkeys.loc[dfkeys["Key"] == key, "Cat"] = cat
    #dfkeys["SubCat"] = ""
    dfkeys.to_csv(f"{file_prefix}_{sheet_name}_keys.csv")

# notebook section

#%%
print("hello")
    #print(df.head())



if __name__ == "__main__":
    '''
    Note: post processing with "fill_cat" function is required to fill the category column
    before running the "get_sums" function
    '''
    #manage_keys(visa_sheet)
    #manage_keys(bank_sheet)


    # 1. get the keys
    #parse_xlsx(data_dir, stmts_fn, bank_sheet, func="get_keys")
    # 2. collect the existing keys
    #parse_xlsx(data_dir, stmts_fn, bank_sheet, func="collect_keys")
    #parse_xlsx(data_dir, stmts_fn, bank_sheet, func="fill_cat")
    #parse_xlsx(data_dir, stmts_fn, bank_sheet, func="get_all")
    # parse_xlsx(data_dir, stmts_fn, bank_sheet, func="get_sums")
    # Visa
    #parse_xlsx(data_dir, stmts_fn, visa_sheet, func="get_keys")
    #parse_xlsx(data_dir, stmts_fn, visa_sheet, func="fill_cat")
    parse_xlsx(data_dir, stmts_fn, visa_sheet, func="get_sums")