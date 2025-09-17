import pymupdf
from utils.chunker import Chunker
from utils.llm_client import Client
from datetime import datetime
from preprocessor.preprocessor import Preprocessor
from config import config
import logging

logger = logging.RootLogger(logging.DEBUG)

class DataExtractor:
    def __init__(self) -> None:
        self.preprocessor = Preprocessor()

    def _txt_extract(self, filepath: str):
        with open(filepath, encoding='utf-8') as fp:
            txt = fp.read()
            return txt

    def _docx_extract(self, filepath: str):
        pass

    def _doc_extract(self, filepath: str):
        pass

    def _pdf_extract(self, filepath: str, force_ocr: bool = False) -> str:
        txt = ""
        
        doc = pymupdf.open(filepath)
        if not force_ocr:
            for page in doc:
                txt = txt + page.get_text() + " "

        if force_ocr or (txt.strip(" ") == ""):
            for page in doc:
                ocr_page = page.get_textpage_ocr()
                txt = txt + ocr_page.extractText() + "\n "
        return txt
    
    def clean_data(self, data: str):
        chunker = Chunker()
        chunks = chunker.chunk_data(data)

        client = Client()
        prompt = '''Sos un pre-procesador de texto de clase mundial, esta es la informaciion extraida de un pdf, por favor parseala y devolverla en un formato que sea procesable por una inteligencia artificial a modo de RAG.
        La informacion extraida esta generada con saltos de linea innecesarios, caracteres especiales, indices, tabulaciones, notas al pie y descripciones de graficos e imagenes, que pueden ser removidos completamente. Basicamente, elimina todos los textos que no sean utiles para responder preguntas a estudiantes.
        Recorda que los textos pueden incluir temas y formatos multiples, por lo que la lista anterior no es exhaustiva.
        Muy importante: NO REPETIR ESTO, SOLAMENTE LIMPIAR EL TEXTO Y REESCRIBIR SI ES NECESARIO.
        NO INCLUIR LENGUAJE DE MARCACION NI NINGUN TIPO DE FORMATO O CARACTERES ESPECIALES. NUNCA agregues notas ni mensajes como 'aqui esta el resultado'.
        SIEMPRE empezar la respuesta directamente, sin preguntas y acknowledgements. 
        Este es el texto: '''
        time_records = []
        clean_data = ""
        for chunk in chunks:
            
            conversation = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": chunk},
            ]
            st = datetime.now()
            response = client.get_response( messages=conversation)
            ft = datetime.now()
            clean_data = clean_data + " " + response
            
            td = ft-st
            time_records.append({"chunk_size":len(chunk),"time": td})
            logger.debug(td.total_seconds())
        return clean_data, time_records
    
    def _txt_metadata(self, filepath: str):
        data = open(filepath, 'r', encoding="utf-8").read()
        pp = self.preprocessor
        expected_metadata = pp.determine_metadata(data)
        try:
            m = eval(expected_metadata)
            return {"title": m.get("title", ""), "author":m.get("author", ""), "creationDate": m.get("creationDate", "")}
        except (SyntaxError, NameError, TypeError):
            return None
            

    def _pdf_metadata(self, filepath: str):
        doc = pymupdf.open(filepath)
        metadata = {"title": doc.metadata["title"], 
                    "author": doc.metadata["author"],
                    "creationDate":doc.metadata["creationDate"] }
        return metadata
    
    def _complete_metadata(self, filepath, metadata):
        data = open(filepath, 'r', encoding="utf-8").read()
        try:
            expected_metadata = self.preprocessor.complete_metadata(data, metadata)
            m = eval(expected_metadata)
            return {"title": m.get("title", ""), "author":m.get("author", ""), "creationDate": m.get("creationDate", "")}
        except:
            return None 
        

    def extract_data(self, filepath: str) -> str:
        format = (filepath.split(".")[-1]).lower()
        if format == "txt":
            data = self._txt_extract(filepath)
        elif format == "docx":
            pass
        elif format == "pdf":
            data = self._pdf_extract(filepath, force_ocr=False)
        elif format == "doc":
            pass

        return data
    
    def extract_data_ocr    (self, filepath: str) -> str:
        data = self._pdf_extract(filepath, force_ocr=True)
        return data
    
    def extract_metadata(self, filepath: str):
        format = (filepath.split(".")[-1]).lower()
        if format == "txt":
            metadata = self._txt_metadata(filepath)
        elif format == "docx":
            pass
        elif format == "pdf":
            metadata = self._pdf_metadata(filepath)
            if not metadata.get("author") or not metadata.get("title"):
                metadata = self._complete_metadata(filepath, metadata)
        elif format == "doc":
            pass

        return metadata