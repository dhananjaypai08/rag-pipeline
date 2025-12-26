from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict, Any
from enum import Enum


class DataSourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    DATABASE = "database"
    TEXT = "text"
    JSON_SCHEMA = "json_schema"
    HTML = "html"


class Document(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    source: str


class IngestRequest(BaseModel):
    source_type: DataSourceType
    source_path: Optional[str] = None
    content: Optional[str] = None
    database_url: Optional[str] = None
    table_name: Optional[str] = None
    query: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode='after')
    def validate_source(self):
        """Ensure either source_path or content is provided for non-database sources."""
        if self.source_type != DataSourceType.DATABASE:
            if not self.source_path and not self.content:
                raise ValueError("Either source_path or content must be provided")
        return self


class IngestResponse(BaseModel):
    success: bool
    documents_ingested: int
    message: str


class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = None
    filters: Optional[Dict[str, Any]] = None


class SourceChunk(BaseModel):
    content: str
    score: float
    source: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
    query: str

