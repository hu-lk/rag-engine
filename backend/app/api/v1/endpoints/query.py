from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.retrieval import retrieval_service
from app.services.llm import llm_service
from app.schemas.query import QueryRequest, QueryResponse, SourceCitation

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def query_rag(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. Retrieve relevant chunks
        context_chunks = retrieval_service.search_chunks(
            db, request.question, top_k=request.top_k
        )
        
        # 2. Generate answer using context
        answer = llm_service.generate_answer(request.question, context_chunks)
        
        # 3. Format response with citations
        sources = [
            SourceCitation(document_id=c['document_id'], content=c['content'])
            for c in context_chunks
        ]
        
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
