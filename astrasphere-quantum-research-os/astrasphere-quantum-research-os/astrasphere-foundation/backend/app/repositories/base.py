"""Generic async repository (Repository Pattern).

Feature-specific repositories subclass this to get CRUD, pagination,
filtering, sorting, and soft-delete for free while staying free to add
domain-specific queries. Repositories are the only layer that talks
SQLAlchemy directly — services never import the ORM.
"""

import uuid
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.db.base import ModelBase, SoftDeleteMixin

ModelType = TypeVar("ModelType", bound=ModelBase)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self._session = session
        self._model = model

    @property
    def session(self) -> AsyncSession:
        """Exposes the underlying session so services can attach
        related writes (e.g. an audit-log row) to the same
        transaction as a repository mutation."""
        return self._session

    @property
    def _is_soft_deletable(self) -> bool:
        return issubclass(self._model, SoftDeleteMixin)

    def _base_query(self, *, include_deleted: bool = False) -> "Select[tuple[ModelType]]":
        query: Select[tuple[ModelType]] = select(self._model)
        if self._is_soft_deletable and not include_deleted:
            query = query.where(self._soft_delete_column().is_(None))
        return query

    def _soft_delete_column(self) -> ColumnElement[Any]:
        """`deleted_at` only exists on soft-deletable models; accessed
        via getattr (rather than a static attribute reference) because
        `ModelType` isn't statically known to include `SoftDeleteMixin`
        — the `_is_soft_deletable` runtime check is what guarantees
        this is safe to call."""
        column: ColumnElement[Any] = getattr(self._model, "deleted_at")  # noqa: B009
        return column

    async def get(self, entity_id: uuid.UUID, *, include_deleted: bool = False) -> ModelType | None:
        if not self._is_soft_deletable or include_deleted:
            return await self._session.get(self._model, entity_id)
        result = await self._session.execute(self._base_query().where(self._model.id == entity_id))
        return result.scalar_one_or_none()

    async def list_all(self, offset: int = 0, limit: int = 50) -> list[ModelType]:
        result = await self._session.execute(self._base_query().offset(offset).limit(limit))
        return list(result.scalars().all())

    async def list_paginated(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        filters: list[ColumnElement[bool]] | None = None,
        sort_by: ColumnElement[Any] | None = None,
        sort_desc: bool = True,
    ) -> tuple[list[ModelType], int]:
        """Filtered + sorted page of results, plus the total matching
        count (pre-pagination) so the caller can build a `Page` envelope."""
        query = self._base_query()
        count_query = select(func.count()).select_from(self._model)
        if self._is_soft_deletable:
            count_query = count_query.where(self._soft_delete_column().is_(None))

        for condition in filters or []:
            query = query.where(condition)
            count_query = count_query.where(condition)

        if sort_by is not None:
            query = query.order_by(sort_by.desc() if sort_desc else sort_by.asc())
        else:
            query = query.order_by(self._model.created_at.desc())

        query = query.offset(offset).limit(limit)

        total = (await self._session.execute(count_query)).scalar_one()
        result = await self._session.execute(query)
        return list(result.scalars().all()), total

    async def create(self, entity: ModelType) -> ModelType:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: ModelType) -> None:
        """Hard delete. Prefer `soft_delete` for user-facing removal on
        models that support it; this is for genuinely permanent cleanup."""
        await self._session.delete(entity)
        await self._session.flush()

    async def soft_delete(self, entity: ModelType) -> ModelType:
        if not isinstance(entity, SoftDeleteMixin):
            raise TypeError(f"{type(entity).__name__} does not support soft delete.")
        entity.deleted_at = datetime.now(UTC)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity
