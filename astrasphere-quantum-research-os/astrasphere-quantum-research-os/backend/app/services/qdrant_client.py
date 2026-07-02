"""Qdrant vector database client for semantic / similarity search."""

from functools import lru_cache

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qmodels

from app.core.config import settings

VECTOR_SIZE = 1536  # matches common embedding model dimensionality


@lru_cache
def get_qdrant_client() -> AsyncQdrantClient:
    """Return a cached async Qdrant client for the process lifetime."""
    return AsyncQdrantClient(url=settings.qdrant_url)


async def ensure_collection() -> None:
    """Create the research documents collection if it does not already exist."""
    client = get_qdrant_client()
    collections = await client.get_collections()
    existing = {c.name for c in collections.collections}
    if settings.qdrant_collection not in existing:
        await client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=qmodels.VectorParams(size=VECTOR_SIZE, distance=qmodels.Distance.COSINE),
        )


async def ping_qdrant() -> bool:
    """Health-check helper: returns True if Qdrant responds."""
    client = get_qdrant_client()
    try:
        await client.get_collections()
        return True
    except Exception:
        return False
