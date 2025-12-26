from src.models import DataSourceType


def detect_file_type(filename: str) -> DataSourceType:
    extension = filename.lower().split('.')[-1] if '.' in filename else ''

    extension_map = {
        'txt': DataSourceType.TEXT,
        'text': DataSourceType.TEXT,
        'csv': DataSourceType.CSV,
        'json': DataSourceType.JSON,
        'html': DataSourceType.HTML,
        'htm': DataSourceType.HTML,
    }

    file_type = extension_map.get(extension)
    if not file_type:
        raise ValueError(
            f"Unsupported file type: .{extension}. "
            f"Supported types: {', '.join(extension_map.keys())}"
        )

    return file_type
