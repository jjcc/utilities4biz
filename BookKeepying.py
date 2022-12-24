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
visa_fn = os.getenv("BANK_STMTS")
bank_sheet = os.getenv("BKS")
visa_sheet = os.getenv("VSS")


def parse_xlsx(data_dir, visa_fn, visa_sheet):
    vxls_file = pd.ExcelFile(f"{data_dir}/{visa_fn}")
#vxls_file = pd.read_excel(f"{data_dir}/{visa_fn}")

    print(vxls_file.sheet_names)

    df0 = vxls_file.parse(visa_sheet)
    df = df0.fillna("")
    cols = df.columns
    print(cols)

    df["Description"] = df["Description"].apply(remove_trival_chars)

    desc_col = df["Description"]
    desc_vals0 = list(desc_col.values)
    desc_vals = [ x for x in desc_vals0 if "PAYMENT" not in x ]
    desc_set = set(desc_vals)

    open("desc_vals.txt", "w").write("\n".join(desc_set))
    print(df.head())

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
    #s = remove_trival_chars("BOSTON PIZZA # 432")
    #print(s)
    parse_xlsx(data_dir, visa_fn, visa_sheet)