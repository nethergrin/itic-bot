# Setup

1. Create environment
1. Install requirements from requirements.txt
1. Update .env file with credentials
1. Configure the variables in **src/config.py**
1. Copy the bibliography into _DOCS_DIR_ folder
1. Start the server with command 'python src/main.py startserver'

1. Execute the scripts in this order:
    1. Extract data
    1. Clean data
    1. Extract metadata (optional)
    1. Load data



# Overview

This application attempts to provide the following:

* An extractor to extract information used for teaching and courses, in different formats. Result is stored as text representation of such information
* A pre-processor, to improve the quality of those representations and transform it into a dataset that can be later chunked, processed into embeddings and stored in an vector database, with it's associated metadata (whenever possible)
* A client that can be used to retrieve similarity-based results from that vector database and use it to feed a LLM-enabled RAG application
* A chat application that leverages all the other components to be able to receive questions that students may do about the content of the courses and provide answers based on existing bibliography

# Architecture

The architecture of the application consist on 2 main components, a frontend and a backend.

### Frontend
Developed in react + vite. Provides just a chat interface to interact with the backend. No authentication needed

### Backend

The backend services consist in a set of scripts and a FastAPI server (Uvicorn) to provide the API. Most of the configurations are set in the **src/config.py** file. Required API keys are configured in the **.env** file or passed as env variable

The available scripts are:
* Extract Data: reads all data from DOCS_DIR and attempts to extract the text information. Once retrieve, stores in TXT_DIR. Currently only supports PDF files
* Clean Data: uses a set of LLM calls to clean the data and remove any irrelevant or special characters, tables or other elements that may make the information hard to process. Only processes the elements in TXT_DIR
* Extract Metadata: tries to retrieve metadata from the docs in CLEANTEXT_DIR using an LLM call to complete the data. Stores in METADATA_DIR 
* Load DB: chunks, embeds and inserts all data in CLEANTEXT_DIR into a ChromaDB for lookup and RAG. 

Once started, the server provides endpoints to access all of those scripts, and also a /chat endpoint to receive end-user questions.

With those questions, the application performs the following:
1. Retrieves a set of bibliographic chunks based on a semantic search
1. Sends the user question along with the chunks as context to an LLM for processing
1. Returns the response to the user as a json structure

# TO-DO

Tasks that need to be added:
* Add an authorized endpoint to upload new documents into de DOCS_DIR
* Add features to the DataExtractor class in extractor.py to be able to extract data and metadata from .doc and .docx files
* Implement the RecursiveCharacterTextSplitter in the utils/chunker.py
* Verify if the Topic implementation is actually working correctly => UPDATE: it's not. In load_database, have to calculate the topic and add it to the metadata as array
* Use metadata from METADATA_DIR to populate the metadata field during load_database script
* Determine the possibility to replace the vector embeddings from local transformers to a LLM call
