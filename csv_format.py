import os
import pandas as pd
from langchain.schema.document import Document
from document_utils import split_documents

DATA_PATH = "data"

def load_csv_documents():
    documents = []

    # Load CSV files from the DATA_PATH
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".csv"):
            file_path = os.path.join(DATA_PATH, filename)
            df = pd.read_csv(file_path)

            # Convert each row in the CSV to a Document object
            for index, row in df.iterrows():
                content = f"Row {index}: " + " ".join([f"{col}: {value}" for col, value in row.items()])
                documents.append(Document(page_content=content, metadata={"source": filename, "row_index": index}))
            print(f"Loaded CSV Document: {filename}")

    return documents

if __name__ == "__main__":
    # Test loading CSV documents
    documents = load_csv_documents()
    print(f"Total CSV Documents Loaded: {len(documents)}")

    # Split documents into chunks for embedding
    chunks = split_documents(documents)
    print(f"Total Chunks Created from CSVs: {len(chunks)}")
