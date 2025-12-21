#!/bin/bash

QUESTION="${1:-What is the main topic of the documents?}"

curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d "{
    \"question\": \"$QUESTION\",
    \"top_k\": 5
  }" | jq '.'

