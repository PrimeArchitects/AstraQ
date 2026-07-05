"""Tag business logic."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import ConflictError, NotFoundError
from app.models.tag import Tag
from app.models.user import User
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate, TagUpdate
from app.services.base import BaseService


class TagService(BaseService):
    def __init__(self, tag_repo: TagRepository) -> None:
        self.tags = tag_repo

    async def list_tags(self, user: User) -> list[Tag]:
        return await self.tags.list_for_owner(user.id)

    async def get_owned(self, user: User, tag_id: uuid.UUID) -> Tag:
        tag = await self.tags.get(tag_id)
        if tag is None or tag.owner_id != user.id:
            raise NotFoundError("Tag not found.")
        return tag

    async def create_tag(self, user: User, payload: TagCreate) -> Tag:
        if await self.tags.get_by_name(user.id, payload.name) is not None:
            raise ConflictError("A tag with that name already exists.")
        tag = Tag(owner_id=user.id, name=payload.name, color=payload.color)
        tag = await self.tags.create(tag)
        await record_activity(
            self.tags.session,
            user_id=user.id,
            action="create",
            resource_type="tag",
            resource_id=str(tag.id),
        )
        return tag

    async def update_tag(self, user: User, tag_id: uuid.UUID, payload: TagUpdate) -> Tag:
        tag = await self.get_owned(user, tag_id)
        if payload.name is not None and payload.name != tag.name:
            if await self.tags.get_by_name(user.id, payload.name) is not None:
                raise ConflictError("A tag with that name already exists.")
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(tag, field, value)
        await self.tags.session.flush()
        await self.tags.session.refresh(tag)
        return tag

    async def delete_tag(self, user: User, tag_id: uuid.UUID) -> None:
        tag = await self.get_owned(user, tag_id)
        await self.tags.delete(tag)
        await record_activity(
            self.tags.session,
            user_id=user.id,
            action="delete",
            resource_type="tag",
            resource_id=str(tag_id),
        )
