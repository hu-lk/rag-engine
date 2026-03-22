from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import health, documents, query
from app.core.config import settings
from fastapi import FastAPI

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=f"{settings.API_V1_STR}", tags=["health"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])
app.include_router(query.router, prefix=f"{settings.API_V1_STR}/query", tags=["query"])

@app.get("/")
def root():
    return {"message": "Welcome to the RAG Engine API"}
