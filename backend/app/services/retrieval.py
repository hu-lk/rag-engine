from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.models.chunk import Chunk
from app.services.embedding import embedding_service
from typing import List, Dict, Any

class RetrievalService:
    def search_chunks(self, db: Session, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # 1. Generate embedding for query
        query_embedding = embedding_service.generate_query_embedding(query)

        # 2. Perform similarity search using pgvector <-> (L2 distance)
        # Using vector_cosine_ops <=> for cosine distance might be better depending on model
        # Sentence transformers usually work well with cosine similarity
        
        # We'll use the chunks table and join with documents to get metadata if needed
        # order by embedding <-> '[...]' uses L2 distance
        # order by embedding <=> '[...]' uses cosine distance
        
        results = (
            db.query(Chunk)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )

        return [
            {
                "id": chunk.id,
                "content": chunk.content,
                "document_id": chunk.document_id,
                # We can add a score here if needed by calculating it manually or via SQL
            }
            for chunk in results
        ]

retrieval_service = RetrievalService()
