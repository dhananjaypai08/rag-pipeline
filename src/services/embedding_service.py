from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
from src.config import settings


class EmbeddingService:
    def __init__(self, model_name: str = settings.embedding_model_name) -> None:
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)

    def encode_single(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def get_dimension(self) -> int:
        return self.dimension

