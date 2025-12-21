from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
import uuid
from src.config import settings
from src.models import Document, SourceChunk


class VectorStore:
    def __init__(
        self,
        host: str = settings.qdrant_host,
        port: int = settings.qdrant_port,
        collection_name: str = settings.qdrant_collection_name,
    ) -> None:
        self.client = QdrantClient(url=f"http://{host}:{port}")
        self.collection_name = collection_name

    def initialize_collection(self, vector_size: int) -> None:
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def store_documents(
        self, documents: List[Document], embeddings: List[List[float]]
    ) -> None:
        if len(documents) != len(embeddings):
            raise ValueError("Documents and embeddings must have the same length")

        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": doc.content,
                    "source": doc.source,
                    **doc.metadata,
                },
            )
            for doc, embedding in zip(documents, embeddings)
        ]

        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = settings.retrieval_top_k,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SourceChunk]:
        query_filter = None
        if filters:
            conditions = [
                FieldCondition(
                    key=key, match=MatchValue(value=value)
                )
                for key, value in filters.items()
            ]
            if conditions:
                query_filter = Filter(must=conditions)

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
            with_vectors=False,
        )

        chunks = []
        for point in response.points:
            payload = point.payload or {}
            score = point.score if hasattr(point, 'score') else 0.0
            chunks.append(
                SourceChunk(
                    content=payload.get("content", ""),
                    score=float(score) if score is not None else 0.0,
                    source=payload.get("source", "unknown"),
                    metadata={
                        k: v
                        for k, v in payload.items()
                        if k not in ["content", "source"]
                    },
                )
            )

        return chunks

    def delete_collection(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

