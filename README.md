# RAG Engine Pro

A production-style Retrieval-Augmented Generation (RAG) platform using FastAPI, PostgreSQL (pgvector), and Next.js.

## 🚀 Quick Start Instructions

### 1. Prerequisites
- **PostgreSQL**: Ensure PostgreSQL 18 is running on port `5433`.
- **API Key**: Add your `OPENAI_API_KEY` to `backend/.env`.

### 2. Start the Backend (FastAPI)
Open a terminal and run:
```powershell
cd backend
# With python installed (using port 8001 to avoid conflicts)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```
- **Swagger Documentation**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- **Health Check**: [http://127.0.0.1:8001/api/v1/health](http://127.0.0.1:8001/api/v1/health)

### 3. Start the Frontend (Next.js)
Open a **new** terminal and run:
```powershell
cd frontend
npm run dev
```
- **User Interface**: [http://localhost:3000](http://localhost:3000)

## 📂 Project Structure
- `backend/`: FastAPI application, database models, and RAG services.
- `frontend/`: Next.js application with chat and upload UI.

## 🛠️ Tech Stack
- **AI**: OpenAI GPT-4o-mini & Sentence Transformers.
- **Vector Search**: pgvector in PostgreSQL.
- **Backend**: Python 3.13, FastAPI, SQLAlchemy.
- **Frontend**: Next.js 15, Vanilla CSS.

---

## 📖 Detailed System Documentation

### 1. The RAG Pipeline (How it Works)

Retrieval-Augmented Generation (RAG) is a technique that gives an LLM access to specific, up-to-date data. Here's how our system implements it:

#### Step 1: Document Ingestion (The "R" in RAG)
When you upload a PDF:
1.  **Extraction**: The backend uses `pypdf` to pull the raw text from the file.
2.  **Chunking**: Large documents are broken into smaller "chunks" (semantic segments). This ensures the AI can pinpoint specific information and fits within LLM context limits.
3.  **Vectorization (Embedding)**: Each chunk is passed through the `all-MiniLM-L6-v2` model. This converts human language into a "vector" (a list of numbers) that represents its semantic meaning.
4.  **Storage**: These vectors are stored in PostgreSQL using the `pgvector` extension, allowing for incredibly fast similarity searches.

#### Step 2: Retrieval (The Search)
When you ask a question:
1.  The question itself is vectorized using the same embedding model.
2.  The system performs a **Cosine Similarity Search** against all stored chunks in the database.
3.  It finds the top 5 most relevant chunks that likely contain the answer.

#### Step 3: Generation (The "G" in RAG)
1.  The retrieved chunks (context) and your original question are combined into a specialized prompt.
2.  This prompt is sent to OpenAI's `gpt-4o-mini`.
3.  The LLM is strictly instructed to **only** use the provided context to answer, which minimizes "hallucinations" (the AI making things up).

### 2. Frontend Details
- **Dynamic UI**: Uses React state to provide instant feedback during long-running tasks like document processing.
- **Source Citations**: The UI doesn't just show the answer; it displays the exact snippets of text the AI used to form its response, ensuring transparency.

### 3. Backend Details
- **FastAPI**: Provides a high-performance, asynchronous API layer.
- **SQLAlchemy + pgvector**: Combines traditional relational data (document names, IDs) with modern vector search capabilities in a single database.
