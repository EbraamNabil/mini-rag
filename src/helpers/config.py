from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: List[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGO_DB_NAME: str
    
    GENERATION_BACKEND:str
    EMBEDDING_BACKEND:str
    
    OPENAI_API_KEY:str=None
    OPENAI_API_URL:str=None
    COHERE_API_KEY:str=None
    
    GENERATION_MODEL_ID:str=None
    EMBEDDING_MODEL_ID:str=None
    EMBEDDING_MODEL_SIZE:int=None
    IMPUT_DEFAULT_MAX_CHARACTERS:int=None
    GENERATION_DEFAULT_MAX_TOKENS:int=None
    GENERATION_DEFAULT_TEMPERATURE:float=None
    
    
    VECTOR_DB_BACKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_Distance_Method:str=None
    

    
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8"
    )


def get_settings():
    return Settings()