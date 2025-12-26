from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    llm_provider: str = "ollama"
    llm_model_name: str = "llama3.2"
    llm_base_url: str = "http://localhost:11434"
    llm_temperature: float = 0.0
    llm_top_k: int = 1
    llm_top_p: float = 1.0

    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    retrieval_top_k: int = 5
    database_url: Optional[str] = None
    chunk_size: int = 1000
    chunk_overlap: int = 200

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

