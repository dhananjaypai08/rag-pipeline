#!/bin/bash

set -e

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./scripts/setup_venv.sh
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting RAG Pipeline API server..."
echo "Server will be available at http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py

