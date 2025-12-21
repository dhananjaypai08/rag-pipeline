#!/usr/bin/env python3

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"


def print_section(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def print_subsection(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def make_request(method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        sys.exit(1)


def test_health_check() -> None:
    print_section("Step 1: Health Check")
    result = make_request("GET", "/health")
    print(json.dumps(result, indent=2))


def test_ingest_csv() -> int:
    print_section("Step 2: Ingest CSV Data")
    data = {
        "source_type": "csv",
        "source_path": "test_data/sample.csv",
        "metadata": {
            "description": "Sample CSV data for testing"
        }
    }
    result = make_request("POST", "/ingest", data)
    print(json.dumps(result, indent=2))
    count = result.get("documents_ingested", 0)
    print(f"\n✓ Ingested {count} document chunks from CSV")
    return count


def test_ingest_json() -> int:
    print_section("Step 3: Ingest JSON Data")
    data = {
        "source_type": "json",
        "source_path": "test_data/sample.json",
        "metadata": {
            "description": "Sample JSON data for testing"
        }
    }
    result = make_request("POST", "/ingest", data)
    print(json.dumps(result, indent=2))
    count = result.get("documents_ingested", 0)
    print(f"\n✓ Ingested {count} document chunks from JSON")
    return count


def test_ingest_text() -> int:
    print_section("Step 4: Ingest Text Data")
    data = {
        "source_type": "text",
        "source_path": "test_data/sample.txt",
        "metadata": {
            "description": "Sample text file for testing"
        }
    }
    result = make_request("POST", "/ingest", data)
    print(json.dumps(result, indent=2))
    count = result.get("documents_ingested", 0)
    print(f"\n✓ Ingested {count} document chunks from text file")
    return count


def test_query(question: str, top_k: int = 5) -> None:
    print_section(f"Query: {question}")
    data = {
        "question": question,
        "top_k": top_k
    }
    result = make_request("POST", "/query", data)
    print(f"\nAnswer: {result.get('answer', 'N/A')}")
    print(f"\nSources ({len(result.get('sources', []))}):")
    for i, source in enumerate(result.get('sources', []), 1):
        print(f"  [{i}] Score: {source.get('score', 0):.3f} | Source: {source.get('source', 'N/A')}")
        print(f"      Content: {source.get('content', '')[:100]}...")


def main() -> None:
    print("\n" + "=" * 50)
    print("RAG Pipeline - Full Flow Test (Python)")
    print("=" * 50)
    
    test_health_check()
    
    csv_count = test_ingest_csv()
    json_count = test_ingest_json()
    text_count = test_ingest_text()
    
    total_ingested = csv_count + json_count + text_count
    print(f"\n✓ Total documents ingested: {total_ingested}")
    
    test_query("What programming languages are mentioned?", top_k=5)
    test_query("What is RAG?", top_k=3)
    test_query("What databases are mentioned?", top_k=5)
    
    print_section("Full Flow Test Complete!")
    print("✓ All tests passed successfully!")


if __name__ == "__main__":
    main()

