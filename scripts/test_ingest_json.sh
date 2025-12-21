#!/bin/bash

curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "json",
    "source_path": "test_data/sample.json",
    "metadata": {
      "description": "Sample JSON data for testing"
    }
  }'

