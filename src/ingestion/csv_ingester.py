from typing import List, Dict, Any
import pandas as pd
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class CSVIngester(BaseIngester):
    def ingest(self, source_path: str, metadata: Dict[str, Any]) -> List[Document]:
        df = pd.read_csv(source_path)
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
                    source=f"{source_path}:row_{idx}",
                )
            )

        return documents

