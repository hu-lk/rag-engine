from sentence_transformers import SentenceTransformer
from app.core.config import settings
from typing import List
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL_NAME
        self._model = None

    @property
    def model(self):
        if self._model is None:
            print(f"Loading embedding model: {self.model_name}...")
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        
        embeddings = self.model.encode(texts)
        # Convert numpy array to list of lists (floats) for SQLAlchemy/pgvector
        return embeddings.tolist()

    def generate_query_embedding(self, query: str) -> List[float]:
        embedding = self.model.encode([query])[0]
        return embedding.tolist()

embedding_service = EmbeddingService()
