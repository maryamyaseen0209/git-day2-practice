# from __future__ import annotations
# from pydantic import Field
# from pydantic_settings import BaseSettings
# from pydantic import ConfigDict


# from pydantic import Field

# # Add inside your Settings class:
# default_search_limit: int = Field(default=3)
# dual_query_enabled: bool = Field(default=True, validation_alias="DUAL_QUERY_ENABLED")
# normalization_enabled: bool = Field(default=True, validation_alias="NORMALIZATION_ENABLED")
# merged_search_limit: int = Field(default=5, validation_alias="MERGED_SEARCH_LIMIT")

# class Settings(BaseSettings):
#     # Qdrant settings

#     # Qdrant settings
#     qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
#     qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
#     qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
#     qdrant_collection_name: str = Field(default="documents", alias="QDRANT_COLLECTION_NAME")
#     # qdrant_url: str = Field(default="http://127.0.0.1:6333")
#     # qdrant_collection_name: str = Field(default="week2_day13_chunks")
#     # default_search_limit: int = Field(default=3)
    
#     # Embedding settings
#     embedding_model_name: str = Field(
#         default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#     )
    
#     # Groq settings
#     groq_api_key: str = Field(..., validation_alias="GROQ_API_KEY")
#     groq_model_name: str = Field(
#         default="llama-3.1-8b-instant",
#         validation_alias="GROQ_MODEL"
#     )
    
#     model_config = ConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False,
#         extra="ignore"
#     )

#     # Guardrail settings
#     default_search_limit: int = Field(default=3)
#     merged_search_limit: int = Field(default=5)
#     min_top_score_for_answer: float = Field(
#         default=0.55,
#         validation_alias="MIN_TOP_SCORE_FOR_ANSWER"
#     )
#     min_avg_score_for_answer: float = Field(
#         default=0.45,
#         validation_alias="MIN_AVG_SCORE_FOR_ANSWER"
#     )
#     min_results_for_answer: int = Field(
#         default=2,
#         validation_alias="MIN_RESULTS_FOR_ANSWER"
#     )
#     enable_clarify_behavior: bool = Field(
#         default=True,
#         validation_alias="ENABLE_CLARIFY_BEHAVIOR"
#     )
#     enable_refuse_behavior: bool = Field(
#         default=True,
#         validation_alias="ENABLE_REFUSE_BEHAVIOR"
#     )
#     enable_rag_logging: bool = Field(
#         default=True,
#         validation_alias="ENABLE_RAG_LOGGING"
#     )

# settings = Settings()


from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = Field(default="postgresql://maryam205:@localhost:5432/git_day_practice")
    
    # Qdrant settings
    QDRANT_HOST: str = Field(default="localhost")
    QDRANT_PORT: int = Field(default=6333)
    QDRANT_COLLECTION_NAME: str = Field(default="documents")
    
    # LLM settings
    OPENAI_API_KEY: str = Field(default="")
    LLM_MODEL: str = Field(default="gpt-3.5-turbo")
    
    # Guardrail settings
    default_search_limit: int = Field(default=3)
    merged_search_limit: int = Field(default=5)
    min_top_score_for_answer: float = Field(
        default=0.55,
        alias="MIN_TOP_SCORE_FOR_ANSWER"
    )
    min_avg_score_for_answer: float = Field(
        default=0.45,
        alias="MIN_AVG_SCORE_FOR_ANSWER"
    )
    min_results_for_answer: int = Field(
        default=2,
        alias="MIN_RESULTS_FOR_ANSWER"
    )
    enable_clarify_behavior: bool = Field(
        default=True,
        alias="ENABLE_CLARIFY_BEHAVIOR"
    )
    enable_refuse_behavior: bool = Field(
        default=True,
        alias="ENABLE_REFUSE_BEHAVIOR"
    )
    enable_rag_logging: bool = Field(
        default=True,
        alias="ENABLE_RAG_LOGGING"
    )
    
    class Config:
        env_file = ".env"
        extra = "ignore"

# Create a single settings instance
settings = Settings()

# For backward compatibility
def get_settings():
    return settings