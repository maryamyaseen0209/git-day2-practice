from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

# Configuration
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COLLECTION_NAME = "week2_day12_docs"
DATA_FILE = Path("data/day12_documents.json")
CACHE_DIR = Path(".cache/embeddings")
CACHE_FILE = CACHE_DIR / "day12_embedding_cache.json"
HF_CACHE_DIR = Path(".cache/huggingface")
QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")


def sha256_text(text: str) -> str:
    """Create a unique hash for each text"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_embedding_cache() -> dict[str, list[float]]:
    """Load cached embeddings if they exist"""
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}


def save_embedding_cache(cache: dict[str, list[float]]) -> None:
    """Save embeddings to cache"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_documents() -> list[dict[str, Any]]:
    """Load the sample documents"""
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def get_model() -> SentenceTransformer:
    """Load the sentence transformer model (uses cache)"""
    os.environ.setdefault("HF_HOME", str(HF_CACHE_DIR.resolve()))
    return SentenceTransformer(MODEL_NAME)


def get_or_compute_embeddings(
    model: SentenceTransformer,
    documents: list[dict[str, Any]],
) -> list[list[float]]:
    """Get embeddings from cache or compute new ones"""
    cache = load_embedding_cache()
    vectors: list[list[float]] = []

    for doc in documents:
        text = doc["text"]
        key = sha256_text(text)

        if key in cache:
            # Use cached embedding
            vector = cache[key]
            print(f"✓ Cached: {text[:30]}...")
        else:
            # Compute new embedding
            vector = model.encode(text, normalize_embeddings=True).tolist()
            cache[key] = vector
            print(f"🆕 New: {text[:30]}...")

        vectors.append(vector)

    save_embedding_cache(cache)
    return vectors


def recreate_collection(client: QdrantClient, vector_size: int) -> None:
    """Create or recreate the Qdrant collection"""
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection: {COLLECTION_NAME}")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
    print(f"Created collection: {COLLECTION_NAME} with size {vector_size}")


def upsert_documents(
    client: QdrantClient,
    documents: list[dict[str, Any]],
    vectors: list[list[float]],
) -> None:
    """Upload documents with their vectors to Qdrant"""
    points = []
    for idx, (doc, vector) in enumerate(zip(documents, vectors, strict=False), start=1):
        points.append(
            models.PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "doc_id": doc["id"],
                    "text": doc["text"],
                    "language": doc["language"],
                    "category": doc["category"],
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )
    print(f"Uploaded {len(points)} documents to Qdrant")


def run_search(client: QdrantClient, model: SentenceTransformer, query: str) -> None:
    """Run a semantic search query"""
    # Convert query to embedding
    query_vector = model.encode(query, normalize_embeddings=True).tolist()

    # Search in Qdrant - FIXED METHOD NAME
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=3,
    ).points  # Note: we need .points to access the results

    print(f"\n🔍 Search results for: '{query}'")
    for result in results:
        print(f"  Score: {result.score:.3f} - {result.payload['text'][:60]}...")


def main():
    print("🚀 Starting Day 12 Embeddings Baseline")

    # Load documents
    documents = load_documents()
    print(f"📄 Loaded {len(documents)} documents")

    # Load model
    print("📦 Loading model...")
    model = get_model()

    # Get embeddings (from cache or compute)
    print("🧮 Getting embeddings...")
    vectors = get_or_compute_embeddings(model, documents)

    if not vectors:
        raise RuntimeError("No vectors were generated.")

    # Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL)

    # Create collection
    recreate_collection(client, vector_size=len(vectors[0]))

    # Upload documents
    upsert_documents(client, documents, vectors)

    # Run test searches
    run_search(client, model, "How do I build APIs in Python?")
    run_search(client, model, "programming language for web")
    run_search(client, model, "تلاش کے نظام")  # Urdu for "search systems"

    print("\n✅ Done!")
    print(f"📁 Embedding cache: {CACHE_FILE}")


if __name__ == "__main__":
    main()
