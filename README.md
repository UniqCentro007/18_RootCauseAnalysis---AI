# Root Cause Analysis AI

A FastAPI-based service for IT incident root cause analysis. The application uses a semantic retrieval layer with `sentence-transformers` and an LLM integration via the `groq` client.

## Features

- REST API with `/analyze` for root cause analysis
- `/incidents` endpoint to list stored incidents
- Semantic search of past incident examples
- FastAPI backend with PostgreSQL persistence
- Docker and Python package support

## Requirements

- Python 3.10+
- PostgreSQL (or Docker)
- `GROQ_API_KEY` environment variable for Groq API access

## Quick start (Python)

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set required environment variables:

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rca_db"
export GROQ_API_KEY="your_groq_api_key"
export MODEL_NAME="llama-3.1-8b-instant"
```

4. Run the server:

```bash
python run.py
```

5. Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Quick start (Docker)

1. Create a `.env` file or export the Groq key locally.

2. Launch the stack:

```bash
docker compose up --build
```

3. Access the API at:

```text
http://localhost:8000/docs
```

## Package installation

Install the project as a package and run the CLI entrypoint:

```bash
pip install .
rca-server
```

## Environment variables

- `DATABASE_URL`: PostgreSQL connection string
- `GROQ_API_KEY`: Groq API key required by `app/llm.py`
- `MODEL_NAME`: optional model override (default: `llama-3.1-8b-instant`)

## Project structure

- `app/main.py` - FastAPI application entrypoint
- `app/database.py` - database connection and session management
- `app/models.py` - SQLAlchemy models
- `app/schemas.py` - Pydantic request/response schemas
- `app/llm.py` - LLM wrapper using `groq`
- `app/retrieval.py` - semantic retrieval with FAISS
- `run.py` - programmatic startup entrypoint
- `pyproject.toml` - packaging metadata

## Notes

- The Docker setup in `docker-compose.yml` already includes PostgreSQL and pgAdmin.
- If you do not have a Groq API key, you can still run the service, but the analysis endpoint will fail when calling the LLM.
