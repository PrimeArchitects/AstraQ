"""Vector similarity search endpoints backed by Qdrant."""

from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.research import VectorSearchQuery, VectorSearchResult
from app.services.qdrant_client import get_qdrant_client

router = APIRouter()
logger = get_logger(__name__)


def _fake_embed(text: str) -> list[float]:
    """Deterministic placeholder embedding.

    Replace with a real embedding model (OpenAI, Cohere, local sentence
    transformer, etc.) in production. Kept dependency-free here so the
    scaffold runs without external API keys.
    """
    import hashlib

    digest = hashlib.sha256(text.encode("utf-8")).digest()
    # Expand the 32-byte digest into a 1536-dim pseudo-embedding.
    values = [(b / 255.0) - 0.5 for b in digest]
    repeats = 1536 // len(values) + 1
    return (values * repeats)[:1536]


@router.post("/search", response_model=list[VectorSearchResult], summary="Semantic search")
async def semantic_search(payload: VectorSearchQuery) -> list[VectorSearchResult]:
    """Run a similarity search against the Qdrant research-documents collection."""
    client = get_qdrant_client()
    vector = _fake_embed(payload.query)

    hits = await client.search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=payload.top_k,
    )

    logger.info("vector_search.executed", query=payload.query, hits=len(hits))
    return [
        VectorSearchResult(id=str(hit.id), score=hit.score, payload=hit.payload or {})
        for hit in hits
    ]
