from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class SourceCitation(BaseModel):
    document_id: int
    content: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceCitation]
