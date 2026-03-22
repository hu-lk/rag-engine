from sqlalchemy.orm import Session
from app.db.models.document import Document
from app.db.models.chunk import Chunk
from app.services.embedding import embedding_service
from app.utils.text import chunk_text, clean_text
import pypdf
import io
from typing import BinaryIO

class DocumentIngestService:
    def process_pdf(self, db: Session, file: BinaryIO, filename: str):
        # 1. Create Document record
        db_document = Document(name=filename)
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        # 2. Extract text from PDF
        pdf_reader = pypdf.PdfReader(file)
        full_text = ""
        for page in pdf_reader.pages:
            full_text += page.extract_text() + "\n"

        # 3. Clean and Chunk text
        cleaned_text = clean_text(full_text)
        chunks = chunk_text(cleaned_text)

        if not chunks:
            return db_document

        # 4. Generate Embeddings for chunks
        embeddings = embedding_service.generate_embeddings(chunks)

        # 5. Store Chunks and Embeddings
        for content, embedding in zip(chunks, embeddings):
            db_chunk = Chunk(
                document_id=db_document.id,
                content=content,
                embedding=embedding
            )
            db.add(db_chunk)
        
        db.commit()
        return db_document

document_ingest_service = DocumentIngestService()
