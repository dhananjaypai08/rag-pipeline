#!/bin/bash

curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "source_path": "test_data/sample.txt",
    "metadata": {
      "description": "Sample text file for testing"
    }
  }'

