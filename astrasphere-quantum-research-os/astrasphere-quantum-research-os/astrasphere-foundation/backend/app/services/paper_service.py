"""Research paper business logic: ownership, filtering/sorting/pagination, tag linking."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ColumnElement

from app.core.audit import record_activity
from app.core.exceptions import NotFoundError, ValidationError
from app.models.research_paper import ResearchPaper
from app.models.tag import Tag
from app.models.user import User
from app.repositories.paper_repository import PaperRepository, SortColumn
from app.repositories.tag_repository import TagRepository
from app.schemas.paper import ResearchPaperCreate, ResearchPaperUpdate
from app.services.base import BaseService

if TYPE_CHECKING:
    from app.schemas.paper import PaperMetadataUpsert

SORTABLE_FIELDS: dict[str, SortColumn] = {
    "created_at": ResearchPaper.created_at,
    "updated_at": ResearchPaper.updated_at,
    "title": ResearchPaper.title,
    "year": ResearchPaper.year,
}


class PaperService(BaseService):
    def __init__(self, paper_repo: PaperRepository, tag_repo: TagRepository) -> None:
        self.papers = paper_repo
        self.tags = tag_repo

    async def get_owned(self, user: User, paper_id: uuid.UUID) -> ResearchPaper:
        paper = await self.papers.get_for_owner(paper_id, user.id)
        if paper is None:
            raise NotFoundError("Paper not found.")
        return paper

    async def list_papers(
        self,
        user: User,
        *,
        offset: int,
        limit: int,
        status: str | None = None,
        folder_id: uuid.UUID | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_desc: bool = True,
    ) -> tuple[list[ResearchPaper], int]:
        filters: list[ColumnElement[bool]] = []
        if status is not None:
            filters.append(ResearchPaper.status == status)
        if folder_id is not None:
            filters.append(ResearchPaper.folder_id == folder_id)
        if search:
            filters.append(ResearchPaper.title.ilike(f"%{search}%"))

        sort_col = SORTABLE_FIELDS.get(sort_by, ResearchPaper.created_at)
        return await self.papers.list_paginated_with_relations(
            owner_id=user.id,
            offset=offset,
            limit=limit,
            extra_filters=filters,
            sort_by=sort_col,
            sort_desc=sort_desc,
        )

    async def _resolve_tags(self, user: User, tag_ids: list[uuid.UUID]) -> list[Tag]:
        if not tag_ids:
            return []
        tags = await self.tags.get_many_by_ids(user.id, tag_ids)
        if len(tags) != len(set(tag_ids)):
            raise ValidationError("One or more tags were not found.")
        return tags

    async def create_paper(self, user: User, payload: ResearchPaperCreate) -> ResearchPaper:
        tags = await self._resolve_tags(user, payload.tag_ids)
        paper = ResearchPaper(
            owner_id=user.id,
            title=payload.title,
            authors=payload.authors,
            venue=payload.venue,
            year=payload.year,
            folder_id=payload.folder_id,
            status=payload.status,
            tags=tags,
        )
        paper = await self.papers.create(paper)
        await self.papers.session.refresh(paper, attribute_names=["tags", "metadata_record"])
        await record_activity(
            self.papers.session,
            user_id=user.id,
            action="create",
            resource_type="research_paper",
            resource_id=str(paper.id),
            extra_data={"title": paper.title},
        )
        return paper

    async def update_paper(
        self, user: User, paper_id: uuid.UUID, payload: ResearchPaperUpdate
    ) -> ResearchPaper:
        paper = await self.get_owned(user, paper_id)
        data = payload.model_dump(exclude_unset=True, exclude={"tag_ids"})
        for field, value in data.items():
            setattr(paper, field, value)

        if payload.tag_ids is not None:
            paper.tags = await self._resolve_tags(user, payload.tag_ids)

        await self.papers.session.flush()
        await self.papers.session.refresh(
            paper, attribute_names=["updated_at", "tags", "metadata_record"]
        )
        await record_activity(
            self.papers.session,
            user_id=user.id,
            action="update",
            resource_type="research_paper",
            resource_id=str(paper.id),
        )
        return paper

    async def delete_paper(self, user: User, paper_id: uuid.UUID) -> None:
        paper = await self.get_owned(user, paper_id)
        await self.papers.soft_delete(paper)
        await record_activity(
            self.papers.session,
            user_id=user.id,
            action="delete",
            resource_type="research_paper",
            resource_id=str(paper_id),
        )

    async def upsert_metadata(
        self, user: User, paper_id: uuid.UUID, payload: "PaperMetadataUpsert"
    ) -> ResearchPaper:
        """Create or replace the enrichment metadata row for a paper.
        Kept on this service (not a separate PaperMetadata service)
        since metadata never exists independent of its parent paper."""
        from app.models.paper_metadata import PaperMetadata

        paper = await self.get_owned(user, paper_id)
        data = payload.model_dump()

        if paper.metadata_record is None:
            paper.metadata_record = PaperMetadata(paper_id=paper.id, **data)
        else:
            for field, value in data.items():
                setattr(paper.metadata_record, field, value)

        await self.papers.session.flush()
        await self.papers.session.refresh(paper, attribute_names=["metadata_record"])
        return paper
