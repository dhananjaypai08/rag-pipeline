# RAG Pipeline System

A production-ready, modular Retrieval-Augmented Generation (RAG) pipeline built with Python, featuring multi-source data ingestion, vector storage with Qdrant, and LLM integration via Ollama.

## Features

- **Multi-Source Data Ingestion**: Support for CSV, JSON, text files, and database connections
- **Vector Storage**: Efficient embedding storage and retrieval using Qdrant
- **Type-Safe**: Full type hints with mypy support
- **Modular Architecture**: Clean separation of concerns with dependency injection
- **RESTful API**: FastAPI-based endpoints for ingestion and querying
- **Deterministic Responses**: Configurable LLM parameters for consistent outputs
- **Production-Ready**: Error handling, validation, and scalable design

## Architecture

```
src/
├── api/              # FastAPI application and routes
├── config.py         # Configuration management
├── ingestion/        # Data ingestion modules (CSV, JSON, DB, Text)
├── models.py         # Pydantic models for type safety
├── pipeline/         # RAG and ingestion pipelines
└── services/         # Core services (embedding, vector store, LLM, chunking)
```

## Prerequisites

- Python 3.10+
- Docker (for Qdrant)
- Ollama (for LLM inference)
- 8GB+ RAM recommended

## Quick Start

### 1. Setup Test Environment (Qdrant & Ollama)

```bash
chmod +x scripts/setup_test_environment.sh
./scripts/setup_test_environment.sh
```

This script will:
- Start Qdrant in a Docker container (handles existing containers)
- Install Ollama (if not present)
- Start Ollama service
- Pull the llama3.2 model (if not already present)
- Create `.env` file from `.env.example`

### 2. Setup Virtual Environment and Install Dependencies

```bash
./scripts/setup_venv.sh
```

This will:
- Create a Python virtual environment
- Install all required dependencies

### 3. Configure Environment

The `.env` file will be created automatically from `.env.example` during setup. Edit `.env` if you need to change default settings (optional).

### 4. Start the API Server

```bash
./scripts/start_server.sh
```

Or manually:

```bash
source venv/bin/activate
python main.py
```

The API will be available at `http://localhost:8000`

### 5. View API Documentation

Open your browser to:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

### Data Ingestion

#### Ingest CSV File

```bash
chmod +x scripts/test_ingest_csv.sh
./scripts/test_ingest_csv.sh
```

Or using curl directly:

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "csv",
    "source_path": "test_data/sample.csv",
    "metadata": {
      "description": "Sample CSV data"
    }
  }'
```

#### Ingest JSON File

```bash
chmod +x scripts/test_ingest_json.sh
./scripts/test_ingest_json.sh
```

#### Ingest Text File

```bash
chmod +x scripts/test_ingest_text.sh
./scripts/test_ingest_text.sh
```

#### Ingest from Database

```bash
chmod +x scripts/test_ingest_database.sh
./scripts/test_ingest_database.sh
```

Or with custom query:

```bash
curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "database",
    "database_url": "postgresql://user:password@localhost:5432/dbname",
    "query": "SELECT * FROM users WHERE active = true",
    "metadata": {
      "description": "Active users from database"
    }
  }'
```

### Query the RAG System

```bash
chmod +x scripts/test_query.sh
./scripts/test_query.sh "What programming languages are mentioned?"
```

Or with a custom question:

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "top_k": 5
  }'
```

### Health Check

```bash
chmod +x scripts/test_health.sh
./scripts/test_health.sh
```

### Run Full Flow Test

Test the complete pipeline with all data sources:

**Using Bash:**
```bash
chmod +x scripts/test_full_flow.sh
./scripts/test_full_flow.sh
```

**Using Python:**
```bash
python scripts/test_full_flow.py
# or
chmod +x scripts/test_full_flow.py
./scripts/test_full_flow.py
```

## API Endpoints

### POST `/api/v1/ingest`

Ingest data from various sources.

**Request Body:**
```json
{
  "source_type": "csv|json|text|database|json_schema",
  "source_path": "path/to/file" (required for file types),
  "database_url": "postgresql://..." (required for database),
  "table_name": "table_name" (optional, alternative to query),
  "query": "SELECT * FROM ..." (optional, alternative to table_name),
  "metadata": {
    "key": "value"
  }
}
```

**Response:**
```json
{
  "success": true,
  "documents_ingested": 42,
  "message": "Successfully ingested 42 document chunks"
}
```

### POST `/api/v1/query`

Query the RAG system with a question.

**Request Body:**
```json
{
  "question": "Your question here",
  "top_k": 5 (optional, default: 5),
  "filters": {
    "key": "value" (optional, for filtering results)
  }
}
```

**Response:**
```json
{
  "answer": "Generated answer based on context",
  "sources": [
    {
      "content": "Retrieved chunk content",
      "score": 0.85,
      "source": "source_identifier",
      "metadata": {}
    }
  ],
  "query": "Your original question"
}
```

### GET `/api/v1/health`

Health check endpoint.

## Configuration

Edit `.env` file to customize:

```env
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=documents
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL_NAME=llama3.2
LLM_BASE_URL=http://localhost:11434
LLM_TEMPERATURE=0.0
LLM_TOP_K=1
LLM_TOP_P=1.0
RETRIEVAL_TOP_K=5
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Type Checking

Run mypy for type checking:

```bash
mypy src/
```

## Project Structure

```
RAG-pipeline/
├── src/
│   ├── api/              # API layer
│   │   ├── app.py        # FastAPI application
│   │   ├── routes.py     # API endpoints
│   │   └── dependencies.py  # Dependency injection
│   ├── ingestion/        # Data ingestion
│   │   ├── base_ingester.py
│   │   ├── csv_ingester.py
│   │   ├── json_ingester.py
│   │   ├── text_ingester.py
│   │   ├── database_ingester.py
│   │   └── ingestion_factory.py
│   ├── pipeline/         # Business logic
│   │   ├── rag_pipeline.py
│   │   └── ingestion_pipeline.py
│   ├── services/         # Core services
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   ├── llm_service.py
│   │   └── chunking_service.py
│   ├── config.py         # Configuration
│   └── models.py         # Data models
├── scripts/              # Test scripts
├── test_data/            # Sample test data
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
└── README.md           # This file
```

## Design Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Dependency Injection**: Services are injected via FastAPI dependencies
3. **Type Safety**: Full type hints with Pydantic models
4. **Factory Pattern**: Ingestion factory for extensible data source support
5. **Interface Segregation**: Base classes define clear contracts
6. **Error Handling**: Comprehensive error handling at all layers

## Supported Data Sources

- **CSV**: Automatically converts rows to documents
- **JSON**: Recursively processes nested JSON structures
- **Text Files**: Plain text document ingestion
- **Databases**: PostgreSQL, MySQL via SQLAlchemy
- **JSON Schema**: Treated as JSON with schema metadata

## Performance Considerations

- Embeddings are generated in batches for efficiency
- Vector search uses cosine similarity for fast retrieval
- Chunking with overlap preserves context across boundaries
- LLM parameters optimized for deterministic, low-latency responses

## Troubleshooting

### Qdrant Connection Error

Ensure Qdrant is running:
```bash
docker ps | grep qdrant
```

If not running:
```bash
docker start qdrant
```

If container name conflict:
```bash
docker rm qdrant
./scripts/setup_test_environment.sh
```

### Ollama Connection Error

Ensure Ollama is running:
```bash
pgrep -x ollama || ollama serve
```

Check if model is available:
```bash
ollama list
```

If model is missing:
```bash
ollama pull llama3.2
```

### Virtual Environment Issues

If virtual environment is not activated:
```bash
source venv/bin/activate
```

To recreate virtual environment:
```bash
rm -rf venv
./scripts/setup_venv.sh
```

### Import Errors

Ensure you're in the project root, virtual environment is activated, and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## License

MIT License

