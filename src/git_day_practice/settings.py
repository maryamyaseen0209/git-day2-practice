from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres123@postgres:5432/appdb"
    qdrant_url: str = "http://qdrant:6333"
    qdrant_collection_name: str = "documents"
    groq_api_key: str = "test_key"
    groq_model: str = "llama-3.1-8b-instant"
    
    # Feature flags
    dual_query_enabled: bool = True
    normalization_enabled: bool = True
    merged_search_limit: int = 5
    
    # RAG settings
    min_top_score_for_answer: float = 0.55
    min_avg_score_for_answer: float = 0.45
    min_results_for_answer: int = 2
    
    # Agent settings
    enable_clarify_behavior: bool = True
    enable_refuse_behavior: bool = True
    enable_rag_logging: bool = True
    enable_agent_loop: bool = True
    enable_agent_logging: bool = True
    max_agent_steps: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
