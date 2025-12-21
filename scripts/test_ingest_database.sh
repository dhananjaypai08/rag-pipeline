#!/bin/bash

curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "database",
    "database_url": "postgresql://user:password@localhost:5432/dbname",
    "table_name": "users",
    "metadata": {
      "description": "Users table from database"
    }
  }'

