from fastapi import HTTPException, Request, Body, APIRouter, BackgroundTasks
from chat.chat_service import ChatService
from utils.scripts import load_database, clean_data, extract_data, extract_metadata
import logging
import asyncio

logger = logging.RootLogger(logging.DEBUG) 
fileHandler = logging.FileHandler('./logs/main.log')
logger.addHandler(fileHandler)

router = APIRouter(prefix="/api")

@router.post("/extractdata")
async def extract_data_endpoint(request: Request, background_tasks: BackgroundTasks):
    '''
        Extracts data from the DOCS_DIR and saves it to the TXT_DIR.
    '''
    try:
        background_tasks.add_task(extract_data)
        return {"message": "Data extraction started successfully."}
    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract data")
    
@router.post("/cleandata")
async def clean_data_endpoint(request: Request):
    '''
        Cleans the data in the TXT_DIR and saves it to the CLEANTEXT_DIR.
    '''
    try:
        clean_data()
        return {"message": "Data cleaning completed successfully."}
    except Exception as e:
        logger.error(f"Error during data cleaning: {e}")
        raise HTTPException(status_code=500, detail="Failed to clean data")
    
@router.post("/loaddb")
async def load_database_endpoint(request: Request):
    '''
        Loads the cleaned text files from CLEANTEXT_DIR into a ChromaDB collection.
    '''
    try:
        load_database()
        return {"message": "Database loading completed successfully."}
    except Exception as e:
        logger.error(f"Error during database loading: {e}")
        raise HTTPException(status_code=500, detail="Failed to load database")


@router.post("/chat")
async def chat( request: Request, body: dict = Body(...)):
    '''
        Starts a chat session with the user.
    '''
    try:
        chat = ChatService()
        messages = body.get("messages", [])
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided in the request body")
        response = chat.get_response(messages)
        if not response:
            raise HTTPException(status_code=500, detail="No response from chat service")
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=400, detail="Invalid request format")
    return {"message": response}