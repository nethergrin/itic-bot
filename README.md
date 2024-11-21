# Setup

1. Create environment
1. Install requirements from requirements.txt
1. Update .env file with credentials



# Overview

This application attempts to provide the following:

* An extractor to extract information used for teaching and courses, in different formats. Result is stored as text representation of such information
* A pre-processor, to improve the quality of those representations and transform it into a dataset that can be later chunked, processed into embeddings and stored in an vector database, with it's associated metadata (whenever possible)
* A client that can be used to retrieve similarity-based results from that vector database and use it to feed a LLM-enabled RAG application
* A chat application that leverages all the other components to be able to receive questions that students may do about the content of the courses and provide answers based on existing bibliography