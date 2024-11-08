import argparse
import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import embedding_function
#from langchain_community.vectorstores import Chroma
from document_utils import split_documents , calculate_chunks_ids
from word_format import load_word_documents
from excel_format import load_excel_documents
#from langchain.vectorstores import Chroma
from langchain_chroma import Chroma






DATA_PATH = "data"
CHROMA_PATH = "chroma"

def main():
    # Check if the database should be cleared (using the --reset flag)
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store
    documents = load_documents()

    # Split documents by type
    pdf_chunks = split_documents([doc for doc in documents if doc.metadata['source'].endswith('.pdf')], 'pdf')
    word_chunks = split_documents([doc for doc in documents if doc.metadata['source'].endswith('.docx')], 'word')
    csv_chunks = split_documents([doc for doc in documents if doc.metadata['source'].endswith('.csv')], 'csv')
    excel_chunks = split_documents([doc for doc in documents if doc.metadata['source'].endswith('.xlsx')], 'excel')
    
    chunks = pdf_chunks + word_chunks + csv_chunks + excel_chunks
    add_to_chroma(chunks)

def load_documents():
    documents = []

    #load PDF docuument
    documents_loader = PyPDFDirectoryLoader(DATA_PATH)
    documents.extend(documents_loader.load())

    # Load Word(docx) data file
    documents.extend(load_word_documents())

    # Load CSV format data file
    #documents.extend(load_csv_documents())

    # load Excel format data file
    documents.extend(load_excel_documents())

    return documents

# function to split the data file in chunks (small part)
def split_documents(documents, datatype):
    if datatype == 'pdf' or datatype == 'word':

        chunk_size = 1200
        chunk_overlap = 100

    elif datatype == 'csv' or datatype == 'excel':

        chunk_size = 800
        chunk_overlap = 0

    else:

        chunk_size = 1000
        chunk_overlap = 50

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return text_splitter.split_documents(documents)

# def split_documents(documents: list[Document]):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1200,
#         chunk_overlap=100,
#         length_function=len,
#     )
#     return text_splitter.split_documents(documents)

# function to add those chunks in chroma database 
def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function()
    )

    # Calculate Page IDs
    chunks_with_ids = calculate_chunks_ids(chunks)

    # Add and update the documents
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Add only documents that don't exist in the DB
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, id=new_chunk_ids)
    else:
        print("No new documents to add")

def calculate_chunks_ids(chunks):
    # This will create IDs like "data/xyz.pdf:6:2"
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the Chunk ID
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page metadata
        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

if __name__ == "__main__":
    main()
