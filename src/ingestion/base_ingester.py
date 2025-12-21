from abc import ABC, abstractmethod
from typing import List
from src.models import Document


class BaseIngester(ABC):
    @abstractmethod
    def ingest(self, source_path: str, metadata: dict) -> List[Document]:
        pass

