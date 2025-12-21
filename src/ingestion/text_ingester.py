from typing import List, Dict, Any
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class TextIngester(BaseIngester):
    def ingest(self, source_path: str, metadata: Dict[str, Any]) -> List[Document]:
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc_metadata = metadata.copy()
        doc_metadata["file_type"] = "text"

        return [
            Document(
                content=content,
                metadata=doc_metadata,
                source=source_path,
            )
        ]

