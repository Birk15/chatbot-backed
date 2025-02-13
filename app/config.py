import os
from dotenv import load_dotenv

load_dotenv(override=True)

print(os.getenv("TEXT_SOURCE_URL"))

class Config:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SOURCE_URL = os.getenv("TEXT_SOURCE_URL")
    INDEX_FILE = os.getenv("INDEX_FILE")
    CHUNKS_FILE = os.getenv("CHUNKS_FILE")
    BERT_API_KEY = os.getenv("BERT_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")