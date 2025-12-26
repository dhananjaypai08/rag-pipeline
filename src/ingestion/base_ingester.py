from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.models import Document


class BaseIngester(ABC):
    @abstractmethod
    def ingest(
        self,
        source_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Ingest data from either a file path or direct content.

        Args:
            source_path: Path to the file to ingest (optional if content is provided)
            content: Direct content to ingest (optional if source_path is provided)
            metadata: Additional metadata to attach to documents

        Returns:
            List of Document objects
        """
        pass

