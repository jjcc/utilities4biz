import re
import camelot
from PyPDF2 import PdfReader
from numpy import outer
import pandas as pd

'''
Process each Visa statement PDF and write the third table to a separate sheet in a single Excel file
'''


data_folder = "data4bkping/"
# File paths for the uploaded PDFs
pdf_files_name = [
    #"TD_BUSINESS_TRAVEL_VISA_6195_Apr_05-2023.pdf",
    #"TD_BUSINESS_TRAVEL_VISA_6195_May_05-2023.pdf",
    #"TD_BUSINESS_TRAVEL_VISA_6195_Jun_05-2023.pdf",
    "TD_BUSINESS_TRAVEL_VISA_6195_Jul_05-2023.pdf",
    #"TD_BUSINESS_TRAVEL_VISA_6195_Aug_08-2023.pdf"
]

pdf_files = [data_folder + pdf_file for pdf_file in pdf_files_name]

class PdfTableExtracgtor:
    def __init__(self, file_path):
        self.file_path = file_path
    # Function to extract tables from a PDF file
    def extract_tables_from_pdf(self):
        # Extracting tables from the PDF
        tables = camelot.read_pdf(self.file_path, pages='all', flavor='stream')
        return [table.df for table in tables]
    
    
    
    # Let's define a function to apply the same process to each PDF
    def  process_third_table(self) -> pd.DataFrame:
        # Extract tables from the PDF
        df_tables = self.extract_tables_from_pdf()
        
        # Process the third table if it exists
        if len(df_tables) >= 3:
            third_table = df_tables[2].iloc[6:]  # Drop the first 7 rows
            third_table.columns = third_table.iloc[0]  # Set the 8th row as the header
            third_table = third_table[1:].reset_index(drop=True)  # Drop the header row from the data
            return third_table
        else:
            return None

output_file = data_folder + "consolidated_transaction_tables_v7.xlsx"
def main():
    excel_writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Loop through all PDF files except the first one (which we have already processed)

    for i, pdf_file in enumerate(pdf_files[0:]):
        extractor = PdfTableExtracgtor(pdf_file)
        third_table_as_df = extractor.process_third_table()
        regex = r"TD_BUSINESS_TRAVEL_VISA_6195_(\w+_\d{2})-2023.pdf"
        month_day = re.search(regex, pdf_files_name[i+1]).group(1)
        print(f"Month,day: {month_day}")
        if third_table_as_df is not None:
            sheet_name = f'PDF_{month_day}_transaction'
            third_table_as_df['AMOUNT($)'] = third_table_as_df['AMOUNT($)'].str.replace('$', '')
            third_table_as_df['AMOUNT($)'] = pd.to_numeric(third_table_as_df['AMOUNT($)'], errors='coerce')
            third_table_as_df.to_excel(excel_writer, sheet_name=sheet_name, index=False)
        
        workbook  = excel_writer.book
        #worksheet = workbook.sheets[sheet_name]
        worksheet = excel_writer.sheets[sheet_name]
        worksheet.set_column('C:C', 35)  # Column C width set to 25
        worksheet.set_column('D:D', 25)  # Column D width set to 25
    # Saving the consolidated Excel file
    excel_writer.save()

if __name__ == "__main__":
    main()

