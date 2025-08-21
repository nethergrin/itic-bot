import chromadb
from chromadb.utils.embedding_functions import sentence_transformer_embedding_function, instructor_embedding_function
from chromadb.utils.embedding_functions.openai_embedding_function import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from config import config
import os

load_dotenv()

class DatabaseClient:
    """A client for interacting with the ChromaDB database."""
    collection_name = None
    chroma_storage = None
    embedding_function = None
    db = None
    current_collection = None
    threshold = None

    def __init__(self):
        self.db = chromadb.PersistentClient(
            path=config['CHROMA_STORAGE']
        )
        self.collection_name = config['COLLECTION_NAME']
        self.chroma_storage = config['CHROMA_STORAGE']

        self.embedding_function = self._get_embedding_function(config['EMBEDDING_FUNCTION'])
        self.db = chromadb.PersistentClient(
            path=self.chroma_storage
            )
        
        self.current_collection = self.db.get_or_create_collection(
            self.collection_name, 
            embedding_function=self.embedding_function
        )

        self.threshold = config.get('CHROMA_THRESHOLD', None)

    def _get_embedding_function(self, embedding_function=None):
        if not embedding_function:
            embedding_function = config.get('EMBEDDING_FUNCTION', 'SENTENCE_TRANSFORMER')
        if embedding_function.upper() == "SENTENCE_TRANSFORMER":
            return sentence_transformer_embedding_function.SentenceTransformerEmbeddingFunction()
        if embedding_function.upper() == "INSTRUCTOR":
            # @TODO: add parameters for the embedding
            return instructor_embedding_function.InstructorEmbeddingFunction()
        if embedding_function.upper() == "OPENAI":
            return OpenAIEmbeddingFunction(
                api_key=os.environ["OPENAI_API_KEY"],
                model_name=config.get('OPENAI_MODEL_NAME', "text-embedding-3-small")
            )
    
        
    def get_documents(self, query, topic=None, n_results=5, threshold=1):
        """
        Retrieves relevant documents based on the query.
        :param query: The query string to search for.
        :param n_results: The number of results to return.
        :param threshold: The distance threshold for filtering results. When empty, all results are accepted. 
        :return: A list of documents that match the query.
        """
        filtered_docs = None
        if topic is not None:
            results = self.current_collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"topics": {"$contains": topic}}
            )

            documents = results['documents'][0]
            distances = results['distances'][0]
            filtered_docs = [
            doc for doc, dist in zip(documents, distances)
                if dist < threshold  # Lower is better if using cosine distance (most common)
            ]
        
        if filtered_docs is None:
            results = self.current_collection.query(
            query_texts=[query],
            n_results=n_results
        )

        documents = results['documents'][0]
        distances = results['distances'][0]
        filtered_docs = [
            doc for doc, dist in zip(documents, distances)
            if dist < threshold  # Lower is better if using cosine distance (most common)
        ]
        return filtered_docs if filtered_docs else ["No relevant documents found."]
        

    
