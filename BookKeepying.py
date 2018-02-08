import pandas as pd

data_dir = "data4bkping/"
visa_fn = "TD_VISA_1747_Only.xlsx"


vxls_file = pd.ExcelFile(data_dir + visa_fn)

print vxls_file.sheet_names

df = vxls_file.parse('Sheet1')

df
