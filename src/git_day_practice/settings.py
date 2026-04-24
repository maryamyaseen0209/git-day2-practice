from __future__ import annotations
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

from pydantic import Field

# Add inside your Settings class:
default_search_limit: int = Field(default=3)
dual_query_enabled: bool = Field(default=True, validation_alias="DUAL_QUERY_ENABLED")
normalization_enabled: bool = Field(default=True, validation_alias="NORMALIZATION_ENABLED")
merged_search_limit: int = Field(default=5, validation_alias="MERGED_SEARCH_LIMIT")

class Settings(BaseSettings):
    # Qdrant settings

    # Qdrant settings
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_collection_name: str = Field(default="documents", alias="QDRANT_COLLECTION_NAME")
    # qdrant_url: str = Field(default="http://127.0.0.1:6333")
    # qdrant_collection_name: str = Field(default="week2_day13_chunks")
    # default_search_limit: int = Field(default=3)
    
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
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
