from langchain_text_splitters import SentenceTransformersTokenTextSplitter, RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import logging

logger = logging.RootLogger(logging.DEBUG)

class Chunker():
    def __init__(self) -> None:
        self._splitter = None
    def _get_splitter(self):
        if self._splitter is None:
            self._splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=20, tokens_per_chunk=350)
        return self._splitter

    def chunk_file(self, file):
        fp = open(file, 'r', encoding='utf-8')
        data = fp.read()
        return self.chunk_data(data)
    
    def chunk_data(self, data):
        splitter = self._get_splitter()
        split_data = splitter.split_text(data)
        return split_data

