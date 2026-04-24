from __future__ import annotations
from git_day_practice.normalization import normalize_roman_urdu

# Mock data for testing
MOCK_CHUNKS = {
    "qdrant_001": {
        "score": 0.95,
        "chunk_id": "qdrant_001",
        "doc_id": "doc_qdrant",
        "title": "What is Qdrant?",
        "language": "en",
        "source": "qdrant_docs",
        "chunk_index": 0,
        "text": "Qdrant is a vector similarity search engine that stores embeddings and performs semantic search."
    },
    "docker_001": {
        "score": 0.92,
        "chunk_id": "docker_001",
        "doc_id": "doc_docker",
        "title": "Docker Compose",
        "language": "en",
        "source": "docker_docs",
        "chunk_index": 0,
        "text": "Docker Compose is a tool for defining and running multi-container Docker applications."
    },
    "rag_001": {
        "score": 0.89,
        "chunk_id": "rag_001",
        "doc_id": "doc_rag",
        "title": "RAG System",
        "language": "en",
        "source": "rag_docs",
        "chunk_index": 0,
        "text": "Retrieval-Augmented Generation (RAG) combines retrieval systems with LLMs for better answers."
    },
}

def search_chunks_mock(query: str, limit: int) -> list[dict]:
    """Mock search that returns relevant chunks based on keywords"""
    query_lower = query.lower()
    results = []
    
    # Keyword matching
    if any(word in query_lower for word in ['qdrant', 'qdrnt', 'kya', 'kia', 'karta', 'krta', 'vector']):
        results.append(MOCK_CHUNKS["qdrant_001"].copy())
    
    if any(word in query_lower for word in ['docker', 'compose', 'container']):
        results.append(MOCK_CHUNKS["docker_001"].copy())
    
    if any(word in query_lower for word in ['retrieval', 'rag', 'jawab', 'answer']):
        results.append(MOCK_CHUNKS["rag_001"].copy())
    
    # If no matches, return a default
    if not results:
        results.append({
            "score": 0.50,
            "chunk_id": "default_001",
            "doc_id": "doc_default",
            "title": "General Information",
            "language": "en",
            "source": "general",
            "chunk_index": 0,
            "text": f"No specific match found for: {query}"
        })
    
    return results[:limit]

def dual_query_search_mock(query: str, limit: int) -> dict:
    """Mock dual query search for testing without Qdrant"""
    original_query = query.strip()
    normalized_query = normalize_roman_urdu(query)
    
    original_results = search_chunks_mock(original_query, limit)
    normalized_results = search_chunks_mock(normalized_query, limit)
    
    # Merge and deduplicate
    all_results = original_results + normalized_results
    seen_chunks = set()
    merged = []
    
    for item in all_results:
        if item["chunk_id"] not in seen_chunks:
            seen_chunks.add(item["chunk_id"])
            merged.append(item)
    
    merged.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "original_query": original_query,
        "normalized_query": normalized_query,
        "results": merged[:limit],
    }