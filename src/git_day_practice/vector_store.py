# # from __future__ import annotations
# # import os
# # from qdrant_client import QdrantClient, models

# # QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")


# # def get_qdrant_client() -> QdrantClient:
# #     return QdrantClient(url=QDRANT_URL)


# # def recreate_collection(
# #     client: QdrantClient, collection_name: str, vector_size: int
# # ) -> None:
# #     if client.collection_exists(collection_name):
# #         client.delete_collection(collection_name)
# #     client.create_collection(
# #         collection_name=collection_name,
# #         vectors_config=models.VectorParams(
# #             size=vector_size,
# #             distance=models.Distance.COSINE,
# #         ),
# #     )

# from __future__ import annotations
# from qdrant_client import QdrantClient
# from git_day_practice.settings import settings

# def get_qdrant_client() -> QdrantClient:
#     return QdrantClient(
#         host=settings.qdrant_host,
#         port=settings.qdrant_port,
#     )

from __future__ import annotations
from qdrant_client import QdrantClient
from git_day_practice.settings import settings

def get_qdrant_client() -> QdrantClient:
    # Use qdrant_url if it exists, otherwise use host and port
    if hasattr(settings, 'qdrant_url') and settings.qdrant_url:
        return QdrantClient(url=settings.qdrant_url)
    elif hasattr(settings, 'qdrant_host') and hasattr(settings, 'qdrant_port'):
        return QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
        )
    else:
        # Default to localhost
        return QdrantClient(location=":memory:")  # Use in-memory for testing