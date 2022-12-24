import pandas as pd
import dotenv
import os

# Load .env file
dotenv.load_dotenv()

# Get the data directory from the .env file
data_dir = os.getenv("DATA_DIR")

# Get the file name from the .env file
visa_fn = os.getenv("BANK_STMTS")


vxls_file = pd.ExcelFile(f"{data_dir}/{visa_fn}")
#vxls_file = pd.read_excel(f"{data_dir}/{visa_fn}")

print(vxls_file.sheet_names)

#df = vxls_file.parse('Sheet1')

