#!/bin/bash

set -e

echo "=========================================="
echo "RAG Pipeline - Full Flow Test"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000/api/v1"

echo "Step 1: Health Check"
echo "-------------------"
curl -s -X GET "${BASE_URL}/health" | jq '.'
echo ""
echo ""

echo "Step 2: Ingest CSV Data"
echo "----------------------"
CSV_RESPONSE=$(curl -s -X POST "${BASE_URL}/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "csv",
    "source_path": "test_data/sample.csv",
    "metadata": {
      "description": "Sample CSV data for testing"
    }
  }')
echo "$CSV_RESPONSE" | jq '.'
CSV_COUNT=$(echo "$CSV_RESPONSE" | jq -r '.documents_ingested')
echo "Ingested $CSV_COUNT document chunks from CSV"
echo ""
echo ""

echo "Step 3: Ingest JSON Data"
echo "----------------------"
JSON_RESPONSE=$(curl -s -X POST "${BASE_URL}/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "json",
    "source_path": "test_data/sample.json",
    "metadata": {
      "description": "Sample JSON data for testing"
    }
  }')
echo "$JSON_RESPONSE" | jq '.'
JSON_COUNT=$(echo "$JSON_RESPONSE" | jq -r '.documents_ingested')
echo "Ingested $JSON_COUNT document chunks from JSON"
echo ""
echo ""

echo "Step 4: Ingest Text Data"
echo "----------------------"
TEXT_RESPONSE=$(curl -s -X POST "${BASE_URL}/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "text",
    "source_path": "test_data/sample.txt",
    "metadata": {
      "description": "Sample text file for testing"
    }
  }')
echo "$TEXT_RESPONSE" | jq '.'
TEXT_COUNT=$(echo "$TEXT_RESPONSE" | jq -r '.documents_ingested')
echo "Ingested $TEXT_COUNT document chunks from text file"
echo ""
echo ""

echo "Step 5: Query - What programming languages are mentioned?"
echo "--------------------------------------------------------"
curl -s -X POST "${BASE_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What programming languages are mentioned?",
    "top_k": 5
  }' | jq '.'
echo ""
echo ""

echo "Step 6: Query - What is RAG?"
echo "----------------------------"
curl -s -X POST "${BASE_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is RAG?",
    "top_k": 3
  }' | jq '.'
echo ""
echo ""

echo "Step 7: Query - What databases are mentioned?"
echo "---------------------------------------------"
curl -s -X POST "${BASE_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What databases are mentioned?",
    "top_k": 5
  }' | jq '.'
echo ""
echo ""

echo "=========================================="
echo "Full Flow Test Complete!"
echo "=========================================="

