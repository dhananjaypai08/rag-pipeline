#!/bin/bash

set -e

echo "Setting up test environment..."

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker to run Qdrant."
    exit 1
fi

echo "Checking Qdrant container..."
if docker ps -a --format '{{.Names}}' | grep -q "^qdrant$"; then
    if docker ps --format '{{.Names}}' | grep -q "^qdrant$"; then
        echo "Qdrant container is already running."
    else
        echo "Starting existing Qdrant container..."
        docker start qdrant
    fi
else
    echo "Creating and starting Qdrant container..."
    docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
fi

echo "Waiting for Qdrant to be ready..."
sleep 5

if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

echo "Checking for llama3.2 model..."
if ollama list | grep -q "llama3.2"; then
    echo "llama3.2 model is already available."
else
    echo "Pulling LLM model (this may take a while)..."
    ollama pull llama3.2
fi

if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Test environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Create virtual environment: python -m venv venv"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Install Python dependencies: pip install -r requirements.txt"
echo "4. Start the API server: python main.py"
echo "5. Run test scripts from the scripts/ directory"

