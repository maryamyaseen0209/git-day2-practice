from __future__ import annotations
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from git_day_practice.settings import settings

print("Loading embedding model...")
model = SentenceTransformer(settings.embedding_model_name)
print("Model loaded")

print("Connecting to Qdrant...")
client = QdrantClient(url=settings.qdrant_url)
print("Connected to Qdrant")

def search_chunks(query: str, limit: int = 3) -> list[dict]:
    print(f"Searching: {query}")
    try:
        query_vec = model.encode(query).tolist()
        
        # Try new API first
        try:
            resp = client.query_points(
                collection_name=settings.qdrant_collection_name,
                query=query_vec,
                limit=limit,
                with_payload=True,
            )
            results = resp.points
        except AttributeError:
            results = client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_vec,
                limit=limit,
                with_payload=True,
            )
        
        formatted = []
        for hit in results:
            p = hit.payload or {}
            formatted.append({
                "score": hit.score,
                "doc_id": p.get("doc_id", ""),
                "chunk_id": p.get("chunk_id", ""),
                "title": p.get("title", ""),
                "language": p.get("language", ""),
                "source": p.get("source", ""),
                "chunk_index": p.get("chunk_index", 0),
                "text": p.get("text", ""),
            })
        print(f"Found {len(formatted)} results")
        return formatted
    except Exception as e:
        print(f"Error: {e}")
        return []
