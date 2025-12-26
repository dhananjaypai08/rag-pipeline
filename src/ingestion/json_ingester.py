from typing import List, Dict, Any, Optional
import json
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class JSONIngester(BaseIngester):
    def ingest(
        self,
        source_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Ingest JSON from either a file path or direct content."""
        if metadata is None:
            metadata = {}

        # Load JSON data from either source
        if content is not None:
            data = json.loads(content)
            source = "direct_json_input"
        elif source_path is not None:
            with open(source_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            source = source_path
        else:
            raise ValueError("Either source_path or content must be provided")

        documents = []
        self._process_json_data(data, source, metadata, documents, "")
        return documents

    def _process_json_data(
        self,
        data: Any,
        source_path: str,
        base_metadata: Dict[str, Any],
        documents: List[Document],
        path_prefix: str,
    ) -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path_prefix}.{key}" if path_prefix else key
                if isinstance(value, (dict, list)):
                    self._process_json_data(
                        value, source_path, base_metadata, documents, current_path
                    )
                else:
                    content = f"{key}: {value}"
                    doc_metadata = base_metadata.copy()
                    doc_metadata["json_path"] = current_path
                    documents.append(
                        Document(
                            content=content,
                            metadata=doc_metadata,
                            source=f"{source_path}:{current_path}",
                        )
                    )
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                current_path = f"{path_prefix}[{idx}]" if path_prefix else f"[{idx}]"
                if isinstance(item, (dict, list)):
                    self._process_json_data(
                        item, source_path, base_metadata, documents, current_path
                    )
                else:
                    content = f"{current_path}: {item}"
                    doc_metadata = base_metadata.copy()
                    doc_metadata["json_path"] = current_path
                    documents.append(
                        Document(
                            content=content,
                            metadata=doc_metadata,
                            source=f"{source_path}:{current_path}",
                        )
                    )

