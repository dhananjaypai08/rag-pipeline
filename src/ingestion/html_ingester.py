from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from src.ingestion.base_ingester import BaseIngester
from src.models import Document


class HTMLIngester(BaseIngester):
    def ingest(
        self,
        source_path: Optional[str] = None,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        if metadata is None:
            metadata = {}

        if content is not None:
            html_content = content
            source = "direct_html_input"
        elif source_path is not None:
            with open(source_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            source = source_path
        else:
            raise ValueError("Either source_path or content must be provided")

        soup = BeautifulSoup(html_content, 'lxml')

        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator='\n', strip=True)
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)

        doc_metadata = metadata.copy()
        doc_metadata["file_type"] = "html"

        return [
            Document(
                content=text,
                metadata=doc_metadata,
                source=source,
            )
        ]
