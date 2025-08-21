from utils.llm_client import Client
from utils.db_client import DatabaseClient

class ChatService:
    def __init__(self):
        pass

    def get_response(self, messages):
        docs = self._retrieve_docs(messages[-1]['content'])
        client = Client()
        context = self._build_context(docs)
        messages.insert(0, {"role": "system", "content": context})
        response = client.get_response(messages=messages)
        return response

    def _build_context(self, docs):

        return ("\n\n").join(docs) if docs else "No relevant documents found."

    def _retrieve_docs(self, query):
        """
        Retrieves relevant documents based on the query.
        This method should be implemented to interact with the vector database or any other storage.
        """
        db = DatabaseClient()
        docs = db.get_documents(query, n_results=5)
        return docs