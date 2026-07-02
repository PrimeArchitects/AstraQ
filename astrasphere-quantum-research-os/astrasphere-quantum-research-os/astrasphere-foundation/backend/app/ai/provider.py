"""AI provider abstraction — architecture placeholder only.

No live model calls happen in this phase. The interface is defined now
so that routers/services built later can depend on `AIProvider` without
caring which vendor backs it, and so the eventual Anthropic integration
is a drop-in implementation rather than a refactor.
"""

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Contract every AI backend (Anthropic, local model, etc.) must satisfy."""

    @abstractmethod
    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Return a single text completion for `prompt`."""

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Return a vector embedding for `text`, for Qdrant-backed semantic search."""


class NullAIProvider(AIProvider):
    """Default no-op provider so the app boots with AI_PROVIDER=none.

    Every method raises deliberately — nothing should silently pretend
    to be an AI feature before one is actually implemented.
    """

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError("AI provider is not yet configured.")

    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError("AI provider is not yet configured.")


def get_ai_provider() -> AIProvider:
    """FastAPI dependency factory. Swaps in a real provider based on settings.AI_PROVIDER."""
    return NullAIProvider()
