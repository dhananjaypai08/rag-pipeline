import logging
from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.services.llm_service import LLMService
from src.services.chunking_service import ChunkingService
from src.pipeline.rag_pipeline import RAGPipeline
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.config import settings

logger = logging.getLogger(__name__)


_embedding_service: EmbeddingService | None = None
_vector_store: VectorStore | None = None
_llm_service: LLMService | None = None
_chunking_service: ChunkingService | None = None
_rag_pipeline: RAGPipeline | None = None
_ingestion_pipeline: IngestionPipeline | None = None


def get_embedding_service() -> EmbeddingService:
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def get_vector_store() -> VectorStore:
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
        embedding_service = get_embedding_service()
        if not embedding_service:
            return _vector_store
        _vector_store.initialize_collection(embedding_service.get_dimension())
    return _vector_store


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_chunking_service() -> ChunkingService:
    global _chunking_service
    if _chunking_service is None:
        _chunking_service = ChunkingService()
    return _chunking_service


def get_rag_pipeline() -> RAGPipeline:
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline(
            embedding_service=get_embedding_service(),
            vector_store=get_vector_store(),
            llm_service=get_llm_service(),
        )
    return _rag_pipeline


def get_ingestion_pipeline() -> IngestionPipeline:
    global _ingestion_pipeline
    if _ingestion_pipeline is None:
        logger.info("Initializing ingestion pipeline and required services...")
        _ingestion_pipeline = IngestionPipeline(
            chunking_service=get_chunking_service(),
            embedding_service=get_embedding_service(),
            vector_store=get_vector_store(),
        )
        logger.info("Ingestion pipeline initialized successfully")
    return _ingestion_pipeline

