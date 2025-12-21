#!/bin/bash

curl -X GET "http://localhost:8000/api/v1/health" | jq '.'

