import pytest
from fastapi.testclient import TestClient
from git_day_practice.api import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_rag_endpoint_with_valid_question():
    """Test RAG endpoint with valid question."""
    response = client.post(
        "/rag",
        json={"question": "What is Qdrant?", "limit": 3}
    )
    assert response.status_code == 200
    body = response.json()
    assert "question" in body
    assert "answer" in body
    assert "sources" in body

def test_rag_endpoint_with_empty_question():
    """Test RAG endpoint with empty question (should fail)."""
    response = client.post(
        "/rag",
        json={"question": "", "limit": 3}
    )
    assert response.status_code == 422  # Validation error

def test_rag_endpoint_with_invalid_limit():
    """Test RAG endpoint with limit > 10 (should fail)."""
    response = client.post(
        "/rag",
        json={"question": "test", "limit": 20}
    )
    assert response.status_code == 422

def test_rag_endpoint_with_limit_1():
    """Test RAG endpoint with limit=1."""
    response = client.post(
        "/rag",
        json={"question": "test", "limit": 1}
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["sources"])