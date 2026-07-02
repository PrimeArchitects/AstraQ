"""Qdrant vector-store connection factory.

Placeholder wiring only — no collections or embedding logic yet. This
exists so the AI/RAG layer (semantic search over papers, datasets, lab
notebooks) has a ready connection point when that work begins.
"""

from qdrant_client import AsyncQdrantClient

from app.core.config import get_settings

_qdrant_client: AsyncQdrantClient | None = None


def get_qdrant() -> AsyncQdrantClient:
    """FastAPI dependency: returns a shared Qdrant client."""
    global _qdrant_client
    if _qdrant_client is None:
        settings = get_settings()
        _qdrant_client = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
    return _qdrant_client
