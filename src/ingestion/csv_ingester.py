from typing import List, Dict, Any, Optional
from io import StringIO
import pandas as pd
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class CSVIngester(BaseIngester):
    def ingest(
        self,
        source_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Ingest CSV from either a file path or direct content."""
        if metadata is None:
            metadata = {}

        # Load CSV data from either source
        if content is not None:
            df = pd.read_csv(StringIO(content))
            source = "direct_csv_input"
        elif source_path is not None:
            df = pd.read_csv(source_path)
            source = source_path
        else:
            raise ValueError("Either source_path or content must be provided")
        documents = []

        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            content_parts = [f"{col}: {val}" for col, val in row_dict.items()]
            content = "\n".join(content_parts)

            doc_metadata = metadata.copy()
            doc_metadata["row_index"] = idx
            doc_metadata["columns"] = list(df.columns)

            documents.append(
                Document(
                    content=content,
                    metadata=doc_metadata,
                    source=f"{source}:row_{idx}",
                )
            )

        return documents

