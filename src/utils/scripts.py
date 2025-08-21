from config import config
from utils.db_client import DatabaseClient
import os, json, logging
from utils.chunker import Chunker
from hashlib import sha256
from extractor.extractor import DataExtractor
from preprocessor.preprocessor import Preprocessor

DOCS_DIR = config['DOCS_DIR']
OCR_DIR = config['OCR_DIR']
TXT_DIR = config['TXT_DIR']
EMBEDDING_FUNCTION = config['EMBEDDING_FUNCTION']
CLEANTEXT_DIR = config['CLEANTEXT_DIR']
METADATA_DIR = config["METADATA_DIR"]

logger = logging.RootLogger(logging.DEBUG) 
fileHandler = logging.FileHandler('./logs/main.log')
logger.addHandler(fileHandler)


def load_database():

    db_client = DatabaseClient()
    db = db_client.db
    collection_name = db_client.collection_name
    """ Loads the cleaned text files from CLEANTEXT_DIR into a ChromaDB collection."""

    collection = db.get_or_create_collection(collection_name, embedding_function=db_client._get_embedding_function())
    files = os.listdir(CLEANTEXT_DIR)
    chunker = Chunker()
    for f in files:
        filepath = os.path.join(CLEANTEXT_DIR, f)
        # @TODO: Use metadata from METADATA_DIR
        # to populate the metadata field
        metadata = {"title":"", "author":"", "creationDate":"", "topics":[]}
        print(filepath)
        chunks = chunker.chunk_file(filepath)
        for chunk in chunks:
            chunk_id = sha256(bytearray(chunk, encoding='utf-8')).hexdigest()
            collection.add(ids=[chunk_id], documents=[chunk], metadatas=[metadata])

def clean_data():
    '''
    Cleans all the files in the TXT_DIR using an LLM prompt. 
    Main purpose is to remove unnecessary characters, line breaks, 
    and other formatting issues that may interfere with the LLM's ability 
    to process the text.
    '''
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
        filename = ".".join([file.split(".")[:-1][0], "txt"])
        with open(os.path.join(CLEANTEXT_DIR, file), 'w') as out:
            out.write(clean_data)

def extract_data():
    '''
    Extracts data from the files in DOCS_DIR and saves them as text files in TXT_DIR.
    '''
    logger.info("Extracting data")
    
    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)
    else:
        if not os.path.isdir(TXT_DIR):
            logger.log(f"{TXT_DIR} exists and is not a directory")
            return False
        
    if os.path.isdir(DOCS_DIR):
        files = os.listdir(DOCS_DIR)
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

def extract_data_ocr():
    '''
    Extracts data from the files in DOCS_DIR and saves them as text files in TXT_DIR.
    Forces the use of OCR for files
    '''
    logger.info("Extracting data from OCR dir")

    if not os.path.exists(TXT_DIR):
        os.mkdir(TXT_DIR)
    else:
        if not os.path.isdir(TXT_DIR):
            logger.log(f"{TXT_DIR} exists and is not a directory")
            return False
    
    if os.path.isdir(OCR_DIR):
        files = os.listdir(OCR_DIR)
        if len(files) == 0:
            logger.info(f"{OCR_DIR} is empty")
            return False
        logger.info(f"{len(files)} files in {OCR_DIR}")
        for file in files:
            source_filepath = os.path.join(OCR_DIR, file)
            txt_filepath = os.path.join(TXT_DIR, file + ".txt")
            ext = DataExtractor()
            extracted_text = ext.extract_data_ocr(source_filepath)
            with open(txt_filepath, 'w', encoding='utf-8') as fp:
                fp.write(extracted_text)

        logger.info(f"Processed {len(files)} files")
    else:
        return False

def extract_metadata():
    '''
    Extracts metadata from the files in CLEANTEXT_DIR and saves them as JSON files in METADATA_DIR.
    '''
    files = os.listdir(CLEANTEXT_DIR)
    for f in files:
        filepath = os.path.join(CLEANTEXT_DIR, f)
        ext = DataExtractor()
        extracted_metadata = ext.extract_metadata(filepath)

        md_filepath = os.path.join(METADATA_DIR, f)
        with open(md_filepath, 'w', encoding='utf-8') as fp:
            json.dump(extracted_metadata, fp)