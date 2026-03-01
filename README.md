# RAG Assistant

A Flask-based Retrieval-Augmented Generation (RAG) assistant that:

- Ingests local `.txt` and `.pdf` documents
- Builds in-memory semantic search with FAISS
- Answers queries using retrieved context plus an Ollama LLM
- Falls back to simple MCP-style tools (`code_tool`, `architecture_tool`)
- Stores conversation history in PostgreSQL via SQLAlchemy

## Features

- RAG pipeline with chunking, embedding, and similarity search
- Query routing agent with:
  - Retrieval-first answer strategy
  - Tool decision layer for code/design requests
  - Direct LLM fallback
- Session-based chat memory persisted in database
- REST API endpoints for health, ingestion, and chat

## Tech Stack

- Python
- Flask
- FAISS (`faiss-cpu`)
- NumPy
- SQLAlchemy + PostgreSQL (`psycopg2-binary`)
- Ollama HTTP API
- PyPDF (`pypdf`)

## Project Structure

```text
backend/
  app.py                  # Flask entrypoint
  api/routes.py           # API routes
  agent/orchestrator.py   # Agent orchestration + tool decisions
  rag/
    loader.py             # Loads text/pdf documents
    chunker.py            # Character-based chunking
    embedder.py           # Ollama embeddings client
    retriever.py          # FAISS vector store
    store.py              # Ingestion helpers + global vector store
    llm.py                # Ollama generation client
  memory/
    database.py           # DB engine/session setup
    models.py             # Conversation model + init_db
    service.py            # Save/fetch conversation messages
  mcp/server.py           # Minimal in-process MCP-like tool registry
  tools/
    code_tool.py
    architecture_tool.py
  documents/              # Seed docs auto-ingested at startup
```

## How It Works

1. App startup (`backend/app.py`):
   - Initializes DB tables
   - Ingests `backend/documents` into FAISS
2. Ingestion (`/ingest`):
   - Accepts text payload
   - Chunks and embeds text
   - Adds vectors/chunks to FAISS
3. Chat (`/chat`):
   - Saves user message to DB
   - Loads recent session history
   - Runs retrieval on query
   - If best distance score is below threshold (`0.8`), answers using retrieved context
   - Otherwise routes to tool/direct LLM path
   - Saves assistant response to DB

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Ollama running locally at `http://localhost:11434`
- Ollama models pulled:
  - `llama3` (generation)
  - `nomic-embed-text` (embeddings)

## Setup

1. Clone and enter the repo:

```bash
git clone <your-repo-url>
cd rag-assistant
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Create `.env` inside `backend/`:

```env
DATABASE_URL=postgresql+psycopg2://<user>:<password>@localhost:5432/<db_name>
```

5. Start Ollama and pull models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

6. Run the app (from `backend/`):

```bash
cd backend
python app.py
```

Server default: `http://127.0.0.1:5000`

## API

### `GET /health`

Returns service status.

Response:

```json
{"status":"OK"}
```

### `POST /ingest`

Ingests raw text into the vector store.

Request body:

```json
{"text":"CAP theorem states that ..."}
```

Response:

```json
{
  "message": "Document ingested successfully",
  "chunks_added": 3
}
```

### `POST /chat`

Asks a question with optional conversation `session_id`.

Request body:

```json
{"session_id":"user1","query":"Explain CAP theorem"}
```

Response:

```json
{"answer":"..."}
```

## Example cURL Commands

```bash
curl -X GET http://127.0.0.1:5000/health

curl -X POST http://127.0.0.1:5000/ingest \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"CAP theorem states that a distributed system can only guarantee two of consistency, availability, and partition tolerance.\"}"

curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"Explain CAP theorem\"}"

curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"user1\", \"query\": \"Why is system design used in 20 words?\"}"
```

## Notes and Current Limitations

- Vector store is in-memory only; embeddings are lost on restart.
- Startup ingestion runs once from `backend/documents`.
- Retrieval uses raw L2 distance with fixed threshold `0.8`; may need tuning.
- No empty-index guard before FAISS search in current implementation.
- Minimal input validation and error handling for upstream Ollama/DB failures.
- Tool routing is keyword-driven before LLM fallback in `Agent.decide`.

## Troubleshooting

- `DATABASE_URL` missing or invalid:
  - Ensure `.env` exists under `backend/` and has a valid SQLAlchemy PostgreSQL URL.
- Ollama connection errors:
  - Confirm Ollama is running on `localhost:11434`.
  - Verify required models are pulled.
- Import/module errors:
  - Run app from inside `backend/` so local imports resolve correctly.
- No useful RAG answers:
  - Add higher quality source documents in `backend/documents`.
  - Tune chunk size/overlap and threshold in code.

## Future Improvements

- Persist FAISS index to disk and reload on startup
- Async/background ingestion for large documents
- Better retrieval scoring and reranking
- Stronger guardrails and structured tool-calling format
- Unit/integration tests and CI pipeline
