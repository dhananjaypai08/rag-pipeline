from typing import List
from src.models import Document
from src.config import settings


class ChunkingService:
    def __init__(
        self, chunk_size: int = settings.chunk_size, chunk_overlap: int = settings.chunk_overlap
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, document: Document) -> List[Document]:
        content = document.content
        if len(content) <= self.chunk_size:
            return [document]

        chunks = []
        start = 0
        content_length = len(content)

        while start < content_length:
            end = min(start + self.chunk_size, content_length)

            if end < content_length:
                last_period = content.rfind(".", start, end)
                last_newline = content.rfind("\n", start, end)

                if last_period > start or last_newline > start:
                    end = max(last_period + 1, last_newline + 1)

            chunk_content = content[start:end].strip()
            if chunk_content:
                chunk_metadata = document.metadata.copy()
                chunk_metadata["chunk_index"] = len(chunks)
                chunk_metadata["chunk_start"] = start
                chunk_metadata["chunk_end"] = end

                chunks.append(
                    Document(
                        content=chunk_content,
                        metadata=chunk_metadata,
                        source=document.source,
                    )
                )

            start = end - self.chunk_overlap
            if start >= content_length:
                break

        return chunks

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        all_chunks = []
        for document in documents:
            chunks = self.chunk_document(document)
            all_chunks.extend(chunks)
        return all_chunks

