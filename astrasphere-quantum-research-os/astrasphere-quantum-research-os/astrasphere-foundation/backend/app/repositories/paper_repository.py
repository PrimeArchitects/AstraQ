from typing import Any
from uuid import UUID

from sqlalchemy import ColumnElement, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload
from sqlalchemy.sql import Select

from app.models.research_paper import ResearchPaper
from app.repositories.base import BaseRepository

# `ResearchPaper.created_at` etc. are `InstrumentedAttribute` at the
# class level, which SQLAlchemy's stubs don't treat as a structural
# subtype of `ColumnElement` even though both support `.desc()`/`.asc()`
# at runtime — this alias covers what callers actually pass.
SortColumn = ColumnElement[Any] | InstrumentedAttribute[Any]


class PaperRepository(BaseRepository[ResearchPaper]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ResearchPaper)

    def _with_relations(self) -> "Select[tuple[ResearchPaper]]":
        return self._base_query().options(
            selectinload(ResearchPaper.tags), selectinload(ResearchPaper.metadata_record)
        )

    async def get_for_owner(self, paper_id: UUID, owner_id: UUID) -> ResearchPaper | None:
        result = await self._session.execute(
            self._with_relations().where(
                ResearchPaper.id == paper_id, ResearchPaper.owner_id == owner_id
            )
        )
        return result.scalar_one_or_none()

    async def list_paginated_with_relations(
        self,
        *,
        owner_id: UUID,
        offset: int,
        limit: int,
        extra_filters: list[ColumnElement[bool]] | None = None,
        sort_by: SortColumn | None = None,
        sort_desc: bool = True,
    ) -> tuple[list[ResearchPaper], int]:
        filters = [ResearchPaper.owner_id == owner_id, *(extra_filters or [])]

        query = self._with_relations()
        count_query = (
            select(func.count())
            .select_from(ResearchPaper)
            .where(ResearchPaper.deleted_at.is_(None))
        )
        for condition in filters:
            query = query.where(condition)
            count_query = count_query.where(condition)

        order_col = sort_by if sort_by is not None else ResearchPaper.created_at
        query = query.order_by(order_col.desc() if sort_desc else order_col.asc())
        query = query.offset(offset).limit(limit)

        total = (await self._session.execute(count_query)).scalar_one()
        result = await self._session.execute(query)
        return list(result.scalars().all()), total
