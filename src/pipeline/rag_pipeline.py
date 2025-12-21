from typing import List, Optional, Dict, Any
from src.services.embedding_service import EmbeddingService
from src.services.vector_store import VectorStore
from src.services.llm_service import LLMService
from src.models import QueryRequest, QueryResponse, SourceChunk


class RAGPipeline:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_service: LLMService,
    ) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_service = llm_service

    def query(self, request: QueryRequest) -> QueryResponse:
        top_k = request.top_k or 5
        query_embedding = self.embedding_service.encode_single(request.question)

        source_chunks = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            filters=request.filters,
        )

        answer = self.llm_service.generate_response(request.question, source_chunks)

        return QueryResponse(
            answer=answer,
            sources=source_chunks,
            query=request.question,
        )

