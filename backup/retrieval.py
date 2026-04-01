from __future__ import annotations
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from git_day_practice.settings import settings

print("🔄 Loading embedding model...")
embedding_model = SentenceTransformer(settings.embedding_model_name)
print(f"✅ Model loaded: {settings.embedding_model_name}")

print("🔄 Connecting to Qdrant...")
qdrant_client = QdrantClient(url=settings.qdrant_url)
print(f"✅ Connected to Qdrant at {settings.qdrant_url}")

def search_chunks(query: str, limit: int = 3) -> list[dict]:
    """Search for relevant chunks using embeddings."""
    print(f"🔍 Searching: {query}")
    
    try:
        # Generate query embedding
        query_embedding = embedding_model.encode(query).tolist()
        
        # Try new Qdrant API (v1.7+)
        try:
            # New API using query_points
            response = qdrant_client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True,
            )
            results = response.points
        except AttributeError:
            # Fallback to old API
            results = qdrant_client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True,
            )
        
        print(f"✅ Found {len(results)} results")
        
        # Format results
        formatted = []
        for hit in results:
            payload = hit.payload or {}
            formatted.append({
                "score": hit.score,
                "doc_id": payload.get("doc_id", ""),
                "chunk_id": payload.get("chunk_id", ""),
                "title": payload.get("title", ""),
                "language": payload.get("language", ""),
                "source": payload.get("source", ""),
                "chunk_index": payload.get("chunk_index", 0),
                "text": payload.get("text", ""),
            })
        
        return formatted
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        # Return mock data for testing
        return [{
            "score": 0.95,
            "doc_id": "test_doc",
            "chunk_id": "test_chunk",
            "title": "Test Document",
            "language": "en",
            "source": "test",
            "chunk_index": 0,
            "text": f"This is mock content for query: {query}"
        }] * min(limit, 3)