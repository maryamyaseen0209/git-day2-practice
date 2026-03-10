import requests

COLLECTION = "week2_day11_vectors"
QDRANT_URL = "http://qdrant:6333"


def main():
    # Delete collection if exists (optional - comment out if you don't want to delete)
    # requests.delete(f"{QDRANT_URL}/collections/{COLLECTION}")

    # Create collection
    create_response = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION}",
        json={"vectors": {"size": 4, "distance": "Cosine"}},
    )
    print(f"Create collection: {create_response.status_code}")

    # Insert points
    points = {
        "points": [
            {
                "id": 1,
                "vector": [0.10, 0.20, 0.30, 0.40],
                "payload": {
                    "doc_id": "A-001",
                    "category": "notes",
                    "source": "wsl",
                    "score": 10,
                },
            },
            {
                "id": 2,
                "vector": [0.11, 0.19, 0.29, 0.39],
                "payload": {
                    "doc_id": "A-002",
                    "category": "notes",
                    "source": "github",
                    "score": 9,
                },
            },
            {
                "id": 3,
                "vector": [0.90, 0.10, 0.05, 0.02],
                "payload": {
                    "doc_id": "B-001",
                    "category": "todo",
                    "source": "wsl",
                    "score": 3,
                },
            },
            {
                "id": 4,
                "vector": [0.88, 0.12, 0.04, 0.01],
                "payload": {
                    "doc_id": "B-002",
                    "category": "todo",
                    "source": "slack",
                    "score": 4,
                },
            },
        ]
    }

    upsert_response = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION}/points?wait=true", json=points
    )
    print(f"Upsert points: {upsert_response.status_code}")

    # Search without filter
    search_query = {
        "vector": [0.10, 0.20, 0.30, 0.40],
        "limit": 3,
        "with_payload": True,
    }

    search_response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search", json=search_query
    )

    if search_response.status_code == 200:
        results = search_response.json()
        print("\nSearch results (no filter):")
        for r in results["result"]:
            print(f"  ID: {r['id']}, Score: {r['score']}, Payload: {r['payload']}")

    # Search with filter
    filtered_query = {
        "vector": [0.10, 0.20, 0.30, 0.40],
        "limit": 10,
        "with_payload": True,
        "filter": {"must": [{"key": "category", "match": {"value": "todo"}}]},
    }

    filtered_response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/search", json=filtered_query
    )

    if filtered_response.status_code == 200:
        results = filtered_response.json()
        print("\nFiltered results (category=todo):")
        for r in results["result"]:
            print(f"  ID: {r['id']}, Score: {r['score']}, Payload: {r['payload']}")


if __name__ == "__main__":
    main()
