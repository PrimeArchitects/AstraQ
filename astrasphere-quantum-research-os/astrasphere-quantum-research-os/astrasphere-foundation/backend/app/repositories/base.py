"""Generic async repository (Repository Pattern).

Feature-specific repositories subclass this to get CRUD for free while
staying free to add domain-specific queries. Repositories are the only
layer that talks SQLAlchemy directly — services never import the ORM.
"""

import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self._session = session
        self._model = model

    async def get(self, entity_id: uuid.UUID) -> ModelType | None:
        return await self._session.get(self._model, entity_id)

    async def list(self, offset: int = 0, limit: int = 50) -> list[ModelType]:
        result = await self._session.execute(select(self._model).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def create(self, entity: ModelType) -> ModelType:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        await self._session.delete(entity)
        await self._session.flush()
