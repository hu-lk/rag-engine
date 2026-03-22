from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
# from app.services.document_ingest import document_ingest_service # Import inside endpoint to avoid circularity if needed
from app.schemas.document import DocumentRead
import io

router = APIRouter()

@router.post("/upload", response_model=DocumentRead)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for now.")
    
    try:
        content = await file.read()
        file_io = io.BytesIO(content)
        
        # We'll import it inside here to avoid potential circular imports if any
        from app.services.document_ingest import document_ingest_service
        
        db_document = document_ingest_service.process_pdf(
            db, file_io, file.filename
        )
        return db_document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
