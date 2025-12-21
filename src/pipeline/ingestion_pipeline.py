from typing import List
from src.models import Document, IngestRequest
from src.ingestion.ingestion_factory import IngestionFactory
from src.ingestion.database_ingester import DatabaseIngester
from src.services.chunking_service import ChunkingService
from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.config import settings


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
            documents = ingester.ingest(source_path="", metadata=request.metadata)
        else:
            if not request.source_path:
                raise ValueError("source_path is required for file-based ingestion")
            documents = ingester.ingest(
                source_path=request.source_path,
                metadata=request.metadata,
            )

        chunked_documents = self.chunking_service.chunk_documents(documents)

        if not chunked_documents:
            return 0

        texts = [doc.content for doc in chunked_documents]
        embeddings = self.embedding_service.encode(texts)
        embedding_list = [emb.tolist() for emb in embeddings]

        self.vector_store.store_documents(chunked_documents, embedding_list)

        return len(chunked_documents)

