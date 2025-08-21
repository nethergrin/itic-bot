import ollama, openai, groq
import os
from dotenv import load_dotenv
from config import config

load_dotenv()

class Client:

    def __init__(self, client = None, host = None, port = None, model = None):
        
        if host is None:
            self.host = config["PREPROCESSOR_HOST"]
        else: 
            self.host = host

        if port is None:
            self.port = config["PREPROCESSOR_PORT"]
        else: 
            self.port = port

        if model is None:
            self.model = config["PREPROCESSOR_MODEL"]
        else: 
            self.model = model
            
        if client is None:
            if config["PREPROCESSOR_CLIENT"] == 'ollama':
                self.client = ollama.Client(f'{self.host}:{self.port}')
            elif config["PREPROCESSOR_CLIENT"] == 'groq':
                import groq
                self.client = groq.Client(api_key=os.environ["GROQ_API_KEY"])
            elif config["PREPROCESSOR_CLIENT"] == 'openai':
                import openai
                self.client = openai.Client(api_key=os.environ["OPENAI_API_KEY"])
            else:
                preprocessor = config["PREPROCESSOR_CLIENT"]
                raise NotImplementedError(f"No client implementation for {preprocessor}")
    
    def get_response(self, messages):
        client_type = type(self.client)
        if ( client_type== openai.OpenAI) or (client_type == groq.Client):
            response = self.client.chat.completions.create(model=self.model, messages=messages)
            content = response.choices[0].message.content
            return content
        elif client_type == ollama.Client:
            response = self.client.chat(model=self.model, messages=messages)
            return response["message"]["content"]