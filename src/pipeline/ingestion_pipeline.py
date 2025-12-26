from typing import List
import logging
from src.models import Document, IngestRequest
from src.ingestion.ingestion_factory import IngestionFactory
from src.ingestion.database_ingester import DatabaseIngester
from src.services.chunking_service import ChunkingService
from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.config import settings

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest(self, request: IngestRequest) -> int:
        logger.info(f"Starting ingestion for source type: {request.source_type.value}")

        ingester = IngestionFactory.create_ingester(
            source_type=request.source_type,
            database_url=request.database_url or settings.database_url,
        )

        if request.source_type.value == "database":
            if not isinstance(ingester, DatabaseIngester):
                raise ValueError("Database ingester type mismatch")
            ingester.set_ingestion_params(
                table_name=request.table_name,
                query=request.query,
            )
            documents = ingester.ingest(metadata=request.metadata)
        else:
            documents = ingester.ingest(
                source_path=request.source_path,
                content=request.content,
                metadata=request.metadata,
            )

        logger.info(f"Loaded {len(documents)} documents, starting chunking...")
        chunked_documents = self.chunking_service.chunk_documents(documents)
        if not chunked_documents:
            logger.warning("No chunks created from documents")
            return 0

        logger.info(f"Created {len(chunked_documents)} chunks, generating embeddings...")
        texts = [doc.content for doc in chunked_documents]
        embeddings = self.embedding_service.encode(texts)
        embedding_list = [emb.tolist() for emb in embeddings]

        logger.info(f"Storing {len(chunked_documents)} chunks in vector database...")
        self.vector_store.store_documents(chunked_documents, embedding_list)
        logger.info(f"Successfully ingested {len(chunked_documents)} document chunks")

        return len(chunked_documents)

