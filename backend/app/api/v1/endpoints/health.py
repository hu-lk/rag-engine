from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Ping the database
        db.execute(text("SELECT 1"))
        
        # Check for pgvector extension
        result = db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
        pgvector_installed = result.scalar() is not None
        
        return {
            "status": "healthy" if pgvector_installed else "degraded",
            "database": "connected",
            "pgvector": "installed" if pgvector_installed else "missing (please install pgvector on your host)"
        }
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
