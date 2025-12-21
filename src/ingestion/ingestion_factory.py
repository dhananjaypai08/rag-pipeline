from typing import Dict, Type
from src.ingestion.base_ingester import BaseIngester
from src.ingestion.csv_ingester import CSVIngester
from src.ingestion.json_ingester import JSONIngester
from src.ingestion.text_ingester import TextIngester
from src.ingestion.database_ingester import DatabaseIngester
from src.models import DataSourceType


class IngestionFactory:
    _ingesters: Dict[DataSourceType, Type[BaseIngester]] = {
        DataSourceType.CSV: CSVIngester,
        DataSourceType.JSON: JSONIngester,
        DataSourceType.TEXT: TextIngester,
        DataSourceType.JSON_SCHEMA: JSONIngester,
    }

    @classmethod
    def create_ingester(
        cls, source_type: DataSourceType, database_url: str = None
    ) -> BaseIngester:
        if source_type == DataSourceType.DATABASE:
            if not database_url:
                raise ValueError("database_url is required for database ingestion")
            return DatabaseIngester(database_url)

        ingester_class = cls._ingesters.get(source_type)
        if not ingester_class:
            raise ValueError(f"No ingester available for source type: {source_type}")

        return ingester_class()

