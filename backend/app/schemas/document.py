from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    name: str

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
