
from __future__ import annotations
import os
from typing import Optional

class Settings:
    """Simple settings class without Pydantic for now."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://maryam205:@localhost:5432/git_day_practice")
    
    # Qdrant
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "documents")

    qdrant_url: str = 'http://qdrant:6333'
    qdrant_collection_name: str = "documents"
    
    # LLM settings
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Agent settings
    ENABLE_AGENT_LOOP: bool = os.getenv("ENABLE_AGENT_LOOP", "true").lower() == "true"
    MAX_AGENT_STEPS: int = int(os.getenv("MAX_AGENT_STEPS", "4"))
    ENABLE_AGENT_LOGGING: bool = os.getenv("ENABLE_AGENT_LOGGING", "true").lower() == "true"
    
    # Retrieval
    RETRIEVAL_LIMIT: int = int(os.getenv("RETRIEVAL_LIMIT", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))

# Create instance
settings = Settings()

# Also add lowercase aliases for compatibility
settings.database_url = settings.DATABASE_URL
settings.qdrant_host = settings.QDRANT_HOST
settings.qdrant_port = settings.QDRANT_PORT
settings.qdrant_collection = settings.QDRANT_COLLECTION
settings.embedding_model_name = settings.EMBEDDING_MODEL_NAME
settings.llm_model_name = settings.LLM_MODEL_NAME
settings.openai_api_key = settings.OPENAI_API_KEY
settings.enable_agent_loop = settings.ENABLE_AGENT_LOOP
settings.max_agent_steps = settings.MAX_AGENT_STEPS
settings.enable_agent_logging = settings.ENABLE_AGENT_LOGGING
settings.retrieval_limit = settings.RETRIEVAL_LIMIT
settings.similarity_threshold = settings.SIMILARITY_THRESHOLD
