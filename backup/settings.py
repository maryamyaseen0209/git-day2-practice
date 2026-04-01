from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Qdrant settings
    qdrant_url: str = Field(default="http://127.0.0.1:6333")
    qdrant_collection_name: str = Field(default="week2_day13_chunks")
    default_search_limit: int = Field(default=3)
    
    # Embedding settings
    embedding_model_name: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # Groq settings
    groq_api_key: str = Field(..., validation_alias="GROQ_API_KEY")
    groq_model_name: str = Field(
        default="llama-3.1-8b-instant",
        validation_alias="GROQ_MODEL"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

# Create settings instance
settings = Settings()