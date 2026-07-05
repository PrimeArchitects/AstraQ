"""Bookmark business logic."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import ConflictError, NotFoundError
from app.models.bookmark import Bookmark
from app.models.user import User
from app.repositories.bookmark_repository import BookmarkRepository
from app.repositories.paper_repository import PaperRepository
from app.schemas.bookmark import BookmarkCreate, BookmarkUpdate
from app.services.base import BaseService


class BookmarkService(BaseService):
    def __init__(self, bookmark_repo: BookmarkRepository, paper_repo: PaperRepository) -> None:
        self.bookmarks = bookmark_repo
        self.papers = paper_repo

    async def list_bookmarks(
        self, user: User, offset: int = 0, limit: int = 20
    ) -> tuple[list[Bookmark], int]:
        return await self.bookmarks.list_paginated_for_user(user.id, offset, limit)

    async def get_owned(self, user: User, bookmark_id: uuid.UUID) -> Bookmark:
        bookmark = await self.bookmarks.get(bookmark_id)
        if bookmark is None or bookmark.user_id != user.id:
            raise NotFoundError("Bookmark not found.")
        return bookmark

    async def create_bookmark(self, user: User, payload: BookmarkCreate) -> Bookmark:
        paper = await self.papers.get_for_owner(payload.paper_id, user.id)
        if paper is None:
            raise NotFoundError("Paper not found.")

        if await self.bookmarks.get_for_user_and_paper(user.id, payload.paper_id) is not None:
            raise ConflictError("This paper is already bookmarked.")

        bookmark = Bookmark(user_id=user.id, paper_id=payload.paper_id, note=payload.note)
        bookmark = await self.bookmarks.create(bookmark)
        await record_activity(
            self.bookmarks.session,
            user_id=user.id,
            action="create",
            resource_type="bookmark",
            resource_id=str(bookmark.id),
        )
        return bookmark

    async def update_bookmark(
        self, user: User, bookmark_id: uuid.UUID, payload: BookmarkUpdate
    ) -> Bookmark:
        bookmark = await self.get_owned(user, bookmark_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(bookmark, field, value)
        await self.bookmarks.session.flush()
        await self.bookmarks.session.refresh(bookmark)
        return bookmark

    async def delete_bookmark(self, user: User, bookmark_id: uuid.UUID) -> None:
        bookmark = await self.get_owned(user, bookmark_id)
        await self.bookmarks.delete(bookmark)
        await record_activity(
            self.bookmarks.session,
            user_id=user.id,
            action="delete",
            resource_type="bookmark",
            resource_id=str(bookmark_id),
        )
