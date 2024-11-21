from utils.chunker import Chunker
import ollama
from datetime import datetime
from utils.llm_client import Client
from config import config
from dotenv import load_dotenv
import os
import json

load_dotenv()

class Preprocessor:

    def __init__(self):
        self.client = Client()

    def complete_metadata(self, data, metadata):
        if len(data)>2000:
            header = data[0:2000]
        else:
            header = data
        prompt = '''Sos un asistente de biblioteca. El texto que se agrega debajo es el principio de un documento, articulo, libro o paper academico. Necesito que completes o corrijas la metadata que se agrega debajo del texto, incluyendo el autor, titulo y fecha de creacion o publicacion, en formato json. Solamente debes proveer lo pedido, sin agregar ninguna respuesta adicional. Asegurate de que la respuesta sea un solo objeto, no una lista, y que tenga solo los atributos solicitados. No añadir caracteres de escape. Mantener todo en español. Ejemplo: {"title":"<Titulo del libro o articulo>","author":"<Autores>", "creationDate":"<fecha>"}.'''
        message =   '''Metadatos actuales: '''+json.dumps(metadata) + ''' \n\n\n Encabezado del libro: ''' + header
        conversation = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ]
        response = self.client.get_response( messages=conversation)
        return response

    def determine_metadata(self, data):
        if len(data)>2000:
            header = data[0:2000]
        else:
            header = data
        prompt = '''El texto que se agrega debajo es el principio de un documento, articulo, libro o paper academico. Necesito que extraigas el autor, titulo y fecha de creacion o publicacion, en formato json. Solamente debes proveer lo pedido, sin agregar ninguna respuesta adicional. Asegurate de que la respuesta sea un solo objeto, no una lista, y que tenga solo los atributos solicitados. No añadir caracteres de escape. Mantener todo en español. Ejemplo: {"title":"<Titulo del libro o articulo>","author":"<Autores>", "creationDate":"<fecha>"}'''
        conversation = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": header},
        ]
        response = self.client.get_response( messages=conversation)
        return response

    def clean_data(self, data):
        chunker = Chunker()
        chunks = chunker.chunk_data(data)

        client = self.client
        
        clean_data = ""

        for chunk in chunks:
            
            conversation = [
                {"role": "system", "content": config["CLEAN_DATA_DEFAULT_PROMPT"]},
                {"role": "user", "content": chunk},
            ]
            response = client.get_response( messages=conversation)
            clean_data = clean_data + " " + response
           
        return clean_data