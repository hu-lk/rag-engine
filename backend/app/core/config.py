from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, validator
from typing import Any, Dict, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "RAG Engine"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: int = 5432
    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        db_url = values.get('DATABASE_URL')
        if db_url:
            return db_url
            
        server = values.get('POSTGRES_SERVER')
        user = values.get('POSTGRES_USER')
        password = values.get('POSTGRES_PASSWORD')
        db = values.get('POSTGRES_DB')
        port = values.get('POSTGRES_PORT')
        
        if all([server, user, password, db]):
            return f"postgresql://{user}:{password}@{server}:{port}/{db}"
        
        return None

    OPENAI_API_KEY: str
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
