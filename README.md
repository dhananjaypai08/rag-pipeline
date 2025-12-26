# RAG Pipeline

Production-grade Retrieval-Augmented Generation system with file upload support.

## Features

- File upload from client machines
- Direct content ingestion via API
- HTML support with text extraction
- Automatic file type detection
- Vector embeddings with semantic search
- LLM-powered question answering

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Services

Start Qdrant vector database:
```bash
docker run -p 6333:6333 -d --name qdrant qdrant/qdrant
```

Start Ollama and pull model:
```bash
ollama serve &
ollama pull llama3.2
```

### 3. Configure Environment

Create `.env` file:
```env
QDRANT_HOST=localhost
QDRANT_PORT=6333
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
LLM_MODEL_NAME=llama3.2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 4. Run Server

```bash
python main.py
```

Server runs on `http://localhost:8000`

## API Usage

### Upload File

```python
import requests

with open('document.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/upload',
        files={'file': f}
    )
print(response.json())
```

Using curl:
```bash
curl -X POST http://localhost:8000/api/v1/upload -F "file=@document.txt"
```

### Ingest Content Directly

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/ingest',
    json={
        'source_type': 'text',
        'content': 'Your content here',
        'metadata': {'description': 'Example'}
    }
)
print(response.json())
```

### Query

```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/query',
    json={'question': 'What is in the documents?', 'top_k': 5}
)
print(response.json())
```

## Supported File Types

- `.txt` - Plain text
- `.csv` - CSV data
- `.json` - JSON data
- `.html` - HTML (text extracted)

## API Endpoints

- `POST /api/v1/upload` - Upload file from client
- `POST /api/v1/ingest` - Ingest content directly
- `POST /api/v1/query` - Query with natural language
- `GET /api/v1/health` - Health check

## Architecture

```
src/
├── api/              # API routes and dependencies
├── ingestion/        # File ingesters (CSV, JSON, TXT, HTML)
├── pipeline/         # Ingestion and RAG pipelines
├── services/         # Core services (embeddings, vector store, LLM)
├── models.py         # Pydantic models
├── config.py         # Configuration
└── utils.py          # Utilities
```

## Examples

### Complete Workflow

```python
import requests

url = 'http://localhost:8000/api/v1'

with open('data.csv', 'rb') as f:
    response = requests.post(f'{url}/upload', files={'file': f})
    print(f"Ingested: {response.json()['documents_ingested']} chunks")

response = requests.post(
    f'{url}/query',
    json={'question': 'Summarize the data', 'top_k': 3}
)
print(f"Answer: {response.json()['answer']}")
```

## License

MIT
