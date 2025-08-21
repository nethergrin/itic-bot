config = {
    "DOCS_DIR": "./test/documents/",
    "OCR_DIR": "./data/ocr/",
    "TXT_DIR": "./test/fulltexts/",
    "EMBEDDING_FUNCTION": "SENTENCE_TRANSFORMER",
    "CLEANTEXT_DIR": "./data/cleantexts/",
    "METADATA_DIR": "./data/metadata/",
    "COLLECTION_NAME": "ITIC-DATA",
    "CHROMA_STORAGE": "./data/chroma_storage",
    "CLEAN_DATA_DEFAULT_PROMPT": '''Sos un pre-procesador de texto de clase mundial, esta es la informaciion extraida de un pdf, por favor parseala y devolverla en un formato que sea procesable por una inteligencia artificial a modo de RAG.
        La informacion extraida esta generada con saltos de linea innecesarios, caracteres especiales, indices, tabulaciones, notas al pie y descripciones de graficos e imagenes, que pueden ser removidos completamente. 
        Basicamente, elimina todos los textos que no sean utiles para responder preguntas a estudiantes.
        Recorda que los textos pueden incluir temas y formatos multiples, por lo que la lista anterior no es exhaustiva.
        Muy importante: NO REPETIR ESTO, SOLAMENTE LIMPIAR EL TEXTO Y REESCRIBIR SI ES NECESARIO.
        NO INCLUIR LENGUAJE DE MARCACION NI NINGUN TIPO DE FORMATO O CARACTERES ESPECIALES. NUNCA agregues notas ni mensajes como 'aqui esta el resultado'.
        SIEMPRE empezar la respuesta directamente, sin preguntas y acknowledgements. 
        Este es el texto: ''',
    "PREPROCESSOR_CLIENT" : "groq",
    "PREPROCESSOR_HOST": "192.168.0.91",
    "PREPROCESSOR_PORT": "11434",
    "PREPROCESSOR_MODEL": "llama-3.1-8b-instant",
    "CHROMA_THRESHOLD": 0.1
}