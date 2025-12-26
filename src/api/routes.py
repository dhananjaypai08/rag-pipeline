from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import Optional
import json
from src.models import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from src.pipeline.rag_pipeline import RAGPipeline
from src.pipeline.ingestion_pipeline import IngestionPipeline
from src.api.dependencies import get_rag_pipeline, get_ingestion_pipeline
from src.utils import detect_file_type

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest_data(
    request: IngestRequest,
    ingestion_pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestResponse:
    try:
        documents_count = ingestion_pipeline.ingest(request)
        return IngestResponse(
            success=True,
            documents_ingested=documents_count,
            message=f"Successfully ingested {documents_count} document chunks",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error during ingestion: {str(e)}"
        )


@router.post("/upload", response_model=IngestResponse)
async def upload_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    ingestion_pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
) -> IngestResponse:
    try:
        file_type = detect_file_type(file.filename)
        print("Detected file type :", file_type)
        content_bytes = await file.read()
        content = content_bytes.decode('utf-8')
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid metadata JSON format")

        metadata_dict["uploaded_filename"] = file.filename
        metadata_dict["upload_method"] = "file_upload"
        request = IngestRequest(
            source_type=file_type,
            content=content,
            metadata=metadata_dict
        )
        documents_count = ingestion_pipeline.ingest(request)
        return IngestResponse(
            success=True,
            documents_ingested=documents_count,
            message=f"Successfully uploaded and ingested {documents_count} document chunks from {file.filename}",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding error. Please ensure the file is UTF-8 encoded.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file upload: {str(e)}")


@router.post("/query", response_model=QueryResponse)
async def query(
    request: QueryRequest,
    rag_pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> QueryResponse:
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        response = rag_pipeline.query(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query: {str(e)}")


@router.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "service": "rag-pipeline"}

