from dotenv import load_dotenv
import sys, logging, typer, uvicorn
from config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import endpoints
from utils.scripts import load_database, clean_data, extract_data, extract_metadata, extract_data_ocr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods, including OPTIONS
    allow_headers=["*"],
)
app.include_router(endpoints.router)

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
    elif operation == "ocr":
        print("OCR")
        extract_data_ocr()
    elif operation == "cleandata":
        print("CleanData")
        clean_data()
    elif operation == "metadata":
        print("Metadata")
        extract_metadata()
    
    elif operation == "loaddb":
        print("LoadDB")
        load_database()
    elif operation == "startserver":
        print("Starting server")
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    typer.run(main)