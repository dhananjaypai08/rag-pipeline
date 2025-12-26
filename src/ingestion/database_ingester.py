from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class DatabaseIngester(BaseIngester):
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url)
        self.table_name: Optional[str] = None
        self.query: Optional[str] = None

    def set_ingestion_params(
        self, table_name: Optional[str] = None, query: Optional[str] = None
    ) -> None:
        self.table_name = table_name
        self.query = query

    def ingest(
        self,
        source_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Ingest data from database. source_path and content parameters are not used."""
        if metadata is None:
            metadata = {}

        if self.query:
            return self._ingest_from_query(self.query, metadata)
        elif self.table_name:
            return self._ingest_from_table(self.table_name, metadata)
        else:
            raise ValueError("Either table_name or query must be provided via set_ingestion_params")

    def _ingest_from_query(self, query: str, metadata: Dict[str, Any]) -> List[Document]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()

        documents = []
        for idx, row in enumerate(rows):
            row_dict = dict(zip(columns, row))
            content_parts = [f"{col}: {val}" for col, val in row_dict.items()]
            content = "\n".join(content_parts)

            doc_metadata = metadata.copy()
            doc_metadata["query_index"] = idx
            doc_metadata["query"] = query

            documents.append(
                Document(
                    content=content,
                    metadata=doc_metadata,
                    source=f"database:query_result_{idx}",
                )
            )

        return documents

    def _ingest_from_table(self, table_name: str, metadata: Dict[str, Any]) -> List[Document]:
        inspector = inspect(self.engine)
        if not inspector.has_table(table_name):
            raise ValueError(f"Table {table_name} does not exist")

        columns = [col["name"] for col in inspector.get_columns(table_name)]
        query = f"SELECT * FROM {table_name}"

        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()

        documents = []
        for idx, row in enumerate(rows):
            row_dict = dict(zip(columns, row))
            content_parts = [f"{col}: {val}" for col, val in row_dict.items()]
            content = "\n".join(content_parts)

            doc_metadata = metadata.copy()
            doc_metadata["table_name"] = table_name
            doc_metadata["row_index"] = idx

            documents.append(
                Document(
                    content=content,
                    metadata=doc_metadata,
                    source=f"database:{table_name}:row_{idx}",
                )
            )

        return documents

