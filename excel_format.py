import os 
import pandas as pd
from langchain.schema.document import Document
from document_utils import split_documents

DATA_PATH = "data"

def load_excel_documents():
    documents = []
    sheet_counter = 1

    for filename in os.listdir(DATA_PATH):
        # Only process files ending with .xlsx and skip hidden files
        if not filename.endswith(".xlsx") or filename.startswith('.'):
            print(f"Skipping non-Excel or hidden file: {filename}")
            continue  # Skip the file if it’s not an Excel file
        file_path = os.path.join(DATA_PATH , filename)
        try:

            # to read the sheets in the excel file
            xls = pd.ExcelFile(file_path , engine= "openpyxl")
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
                content = df.to_string(index=False)

                # Add sheet number to the metadata to simulate it
                metadata = {"source": filename , "page":f"{sheet_counter}: {sheet_name}" }
                sheet_counter += 1

                documents.append(Document(page_content = content , metadata = metadata))
                print(f"Loaded Excel Document: {filename} , sheet: {sheet_name}")

            sheet_counter = 1
        except Exception as e:
            print(f"Error loading Excel file {filename} , {e} ")
    return documents

if __name__ == "__main__":

    #Load Excel documents

    documents = load_excel_documents()
    print(f"Total Excel Documents Loaded: {len(documents)}")

    #function to split doucments
    chunks = split_documents(documents)
    print(f"Total Chunks Created: {len(chunks)}")

    


