import argparse
import os
import shutil
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding_function import embedding_function
from langchain.vectorstores.chroma import Chroma


DATA_PATH = "data"
CHROMA_PATH = "chroma"

def main():
    

    # check if the database should be cleanewd (using the --clear flag)

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset" , action="store_true" , help="Reset the database")
    args = parser.parse_args()
    if args.reset:
        print(" ✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

    

def load_documents():
    documents_loader = PyPDFDirectoryLoader(DATA_PATH)
    return documents_loader.load()


def split_documents(documents:list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function=len,
        is_seperator_regex=False,
    )
    return text_splitter.split_documents(documents)


def add_to_chroma(chunks: list[Document]):

    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding_function()
    )

    #Calculate Page IDs.
    chunks_with_ids = calculate_chunks_ids(chunks)

    # Add and update the documents

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents is DB: {len(existing_ids)}")


    # Add only documents that dont exist in the DB.

    new_chunks = []
    for chunk in chunks_with_ids:
        if  chunk.metedata["id"] not in existing_ids:
            new_chunks.append(chunk)


    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["ids"] for chunk in new_chunks]
        db.add_documents(new_chunks , id=new_chunk_ids)
        db.persist()

    else:
        print("No new documents to add")

def calculate_chunks_ids(chunks):
    
    # This will create Ids like "data/xyz.pdf:6:2"
    # Page source : Page Number : Chunk Index


    last_page_id = None
    current_chunk_index = 0


    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"


        #If the page ID is the same as the last one , increment the index.

        if current_page_id == last_page_id:
            current_chunk_index += 1

        else:
            current_chunk_index = 0


        # Calculate the Chunk ID.
        chunk_id = f"{current_page_id}: {current_chunk_index}"

        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id
    
    return chunk

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()