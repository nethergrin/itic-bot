from os import listdir
import os.path
from dotenv import load_dotenv
import sys
import chromadb
from chromadb.utils.embedding_functions import sentence_transformer_embedding_function, instructor_embedding_function
from utils.chunker import Chunker
from hashlib import sha256
import logging
import typer
import json
from extractor.extractor import DataExtractor
from preprocessor.preprocessor import Preprocessor
from config import config


logger = logging.RootLogger(logging.DEBUG) 
fileHandler = logging.FileHandler('./logs/main.log')
logger.addHandler(fileHandler)

load_dotenv()

DOCS_DIR = config['DOCS_DIR']
TXT_DIR = config['TXT_DIR']
EMBEDDING_FUNCTION = config['EMBEDDING_FUNCTION']
CLEANTEXT_DIR = config['CLEANTEXT_DIR']
METADATA_DIR = config["METADATA_DIR"]
COLLECTION_NAME = config['COLLECTION_NAME']
CHROMA_STORAGE = config['CHROMA_STORAGE']


def get_embedding_function():
    if EMBEDDING_FUNCTION.upper() == "SENTENCE_TRANSFORMER":
        return sentence_transformer_embedding_function.SentenceTransformerEmbeddingFunction()
    if EMBEDDING_FUNCTION.upper() == "INSTRUCTOR":
        # @TODO: add parameters for the embedding
        return instructor_embedding_function.InstructorEmbeddingFunction()

def load_database():
    db = chromadb.PersistentClient(
    path=CHROMA_STORAGE
    )

    collection = db.get_or_create_collection(COLLECTION_NAME, embedding_function=get_embedding_function())
    files = os.listdir(CLEANTEXT_DIR)
    chunker = Chunker()
    for f in files:
        filepath = os.path.join(CLEANTEXT_DIR, f)
        chunks = chunker.chunk_file(filepath)
        for chunk in chunks:
            chunk_id = sha256(bytearray(chunk, encoding='utf-8')).hexdigest()
            collection.add(ids=[chunk_id], documents=[chunk])

def clean_data():
    if not os.path.exists(CLEANTEXT_DIR):
        os.mkdir(CLEANTEXT_DIR)
    elif not os.path.isdir(CLEANTEXT_DIR):
        logger.info(f"{CLEANTEXT_DIR} is not a directory")
        return False
    
    if not os.path.exists(TXT_DIR) or not os.path.isdir(TXT_DIR):
        logger.info(f"{TXT_DIR} is not a directory or does not exist")
        return False

    files = os.listdir(TXT_DIR)
    if len(files) == 0:
        logger.info(f"{TXT_DIR} is empty")
        return False
    
    for file in files:
        
        with open(os.path.join(TXT_DIR, file), 'r') as fp:
            data = fp.read()
            preprocessor = Preprocessor()
            clean_data = preprocessor.clean_data(data)
        filename = ".".join(file.split(".")[:-1], "txt")
        with open(os.path.join(TXT_DIR, file), 'w') as out:
            out.write(clean_data)

def extract_data():
    logger.info("Extracting data")
    
    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)
    else:
        if not os.path.isdir(TXT_DIR):
            logger.log(f"{TXT_DIR} exists and is not a directory")
            return False
        
    if os.path.isdir(DOCS_DIR):
        files = listdir(DOCS_DIR)
        if len(files) == 0:
            logger.info(f"{DOCS_DIR} is empty")
            return False
        logger.info(f"{len(files)} files in {DOCS_DIR}")
        for file in files:
            source_filepath = os.path.join(DOCS_DIR, file)
            txt_filepath = os.path.join(TXT_DIR, file + ".txt")
            ext = DataExtractor()
            extracted_text = ext.extract_data(source_filepath)
            with open(txt_filepath, 'w', encoding='utf-8') as fp:
                fp.write(extracted_text)

        logger.info(f"Processed {len(files)} files")
    else:
        return False

def extract_metadata():
    files = listdir(CLEANTEXT_DIR)
    for f in files:
        filepath = os.path.join(CLEANTEXT_DIR, f)
        ext = DataExtractor()
        extracted_metadata = ext.extract_metadata(filepath)

        md_filepath = os.path.join(METADATA_DIR, f)
        with open(md_filepath, 'w', encoding='utf-8') as fp:
            json.dump(extracted_metadata, fp)

def main(operation: str):
    print(operation)
    print("*"*50)
    args = sys.argv[1:]
    if len(args) == 0:
        print("Missing operation params.  -extractdata, -loaddb")
    if operation == "extractdata":
        print("ExtractData")
        extract_data()
        print("CleanData")
        clean_data()
        print("ExtractMetadata")
        extract_metadata()
    elif operation == "cleandata":
        print("CleanData")
        clean_data()
    elif operation == "metadata":
        print("CleanData")
        extract_metadata()
    elif operation == "loaddb":
        print("LoadDB")
        load_database()


if __name__ == "__main__":
    typer.run(main)