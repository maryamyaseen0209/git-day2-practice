from __future__ import annotations

from functools import lru_cache
from sentence_transformers import SentenceTransformer
from git_day_practice.normalization import normalize_roman_urdu
from git_day_practice.settings import settings
from git_day_practice.vector_store import get_qdrant_client

@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model_name)

def search_chunks(query: str, limit: int) -> list[dict]:
    model = get_embedding_model()
    client = get_qdrant_client()
    
    query_vector = model.encode(query, normalize_embeddings=True).tolist()
    
    # Try different search methods for different qdrant-client versions
    results = None
    
    # Method 1: Try search_points (for older versions)
    if hasattr(client, 'search_points'):
        from qdrant_client.models import SearchRequest
        results = client.search_points(
            collection_name=settings.qdrant_collection_name,
            vector=query_vector,
            limit=limit,
        )
    # Method 2: Try search (for newer versions)
    elif hasattr(client, 'search'):
        try:
            results = client.search(
                collection_name=settings.qdrant_collection_name,
                query_vector=query_vector,
                limit=limit,
            )
        except:
            # Try with vector parameter instead of query_vector
            results = client.search(
                collection_name=settings.qdrant_collection_name,
                vector=query_vector,
                limit=limit,
            )
    # Method 3: Try query_points (for latest versions)
    elif hasattr(client, 'query_points'):
        results = client.query_points(
            collection_name=settings.qdrant_collection_name,
            query=query_vector,
            limit=limit,
        )
        results = results.points if results else []
    else:
        # If no search method found, return empty list
        print(f"Warning: No search method found in QdrantClient")
        return []
    
    # Handle different result formats
    if results is None:
        return []
    
    # Convert to list if needed
    if hasattr(results, 'points'):
        results = results.points
    
    formatted_results: list[dict] = []
    for point in results:
        payload = point.payload or {}
        formatted_results.append({
            "score": float(point.score),
            "doc_id": payload.get("doc_id", ""),
            "chunk_id": payload.get("chunk_id", ""),
            "title": payload.get("title", ""),
            "language": payload.get("language", ""),
            "source": payload.get("source", ""),
            "chunk_index": payload.get("chunk_index", 0),
            "text": payload.get("text", ""),
        })
    return formatted_results

def merge_results(result_sets: list[list[dict]], final_limit: int) -> list[dict]:
    best_by_chunk_id: dict[str, dict] = {}
    
    for result_set in result_sets:
        for item in result_set:
            chunk_id = item["chunk_id"]
            if chunk_id not in best_by_chunk_id:
                best_by_chunk_id[chunk_id] = item
            else:
                if item["score"] > best_by_chunk_id[chunk_id]["score"]:
                    best_by_chunk_id[chunk_id] = item
    
    merged = list(best_by_chunk_id.values())
    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged[:final_limit]

def dual_query_search(query: str, limit: int) -> dict:
    original_query = query.strip()
    normalized_query = normalize_roman_urdu(query)
    
    original_results = search_chunks(original_query, limit)
    normalized_results = search_chunks(normalized_query, limit)
    
    merged_results = merge_results(
        [original_results, normalized_results], 
        final_limit=getattr(settings, 'merged_search_limit', 5)
    )
    
    return {
        "original_query": original_query,
        "normalized_query": normalized_query,
        "results": merged_results,
    }