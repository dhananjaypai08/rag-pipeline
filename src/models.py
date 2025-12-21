from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class DataSourceType(str, Enum):
    CSV = "csv"
    JSON = "json"
    DATABASE = "database"
    TEXT = "text"
    JSON_SCHEMA = "json_schema"


class Document(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    source: str


class IngestRequest(BaseModel):
    source_type: DataSourceType
    source_path: Optional[str] = None
    database_url: Optional[str] = None
    table_name: Optional[str] = None
    query: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


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

