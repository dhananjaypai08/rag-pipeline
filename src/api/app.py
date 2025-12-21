from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="RAG Pipeline API",
    description="Retrieval-Augmented Generation Pipeline with multi-source data ingestion",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1", tags=["rag"])


@app.get("/")
async def root() -> dict:
    return {
        "message": "RAG Pipeline API",
        "version": "1.0.0",
        "endpoints": {
            "ingest": "/api/v1/ingest",
            "query": "/api/v1/query",
            "health": "/api/v1/health",
        },
    }

