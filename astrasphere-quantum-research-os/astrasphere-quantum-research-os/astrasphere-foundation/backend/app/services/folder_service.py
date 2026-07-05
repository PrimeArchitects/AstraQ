"""Folder business logic: ownership enforcement, uniqueness, cascading soft delete."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.folder import Folder
from app.models.user import User
from app.repositories.folder_repository import FolderRepository
from app.schemas.folder import FolderCreate, FolderUpdate
from app.services.base import BaseService


class FolderService(BaseService):
    def __init__(self, folder_repo: FolderRepository) -> None:
        self.folders = folder_repo

    async def list_folders(self, user: User) -> list[Folder]:
        return await self.folders.list_for_owner(user.id)

    async def get_owned(self, user: User, folder_id: uuid.UUID) -> Folder:
        folder = await self.folders.get(folder_id)
        if folder is None or folder.owner_id != user.id:
            raise NotFoundError("Folder not found.")
        return folder

    async def create_folder(self, user: User, payload: FolderCreate) -> Folder:
        if payload.parent_id is not None:
            await self.get_owned(user, payload.parent_id)

        existing = await self.folders.get_by_name(user.id, payload.parent_id, payload.name)
        if existing is not None:
            raise ConflictError("A folder with that name already exists here.")

        folder = Folder(
            owner_id=user.id, name=payload.name, parent_id=payload.parent_id, color=payload.color
        )
        folder = await self.folders.create(folder)
        await record_activity(
            self.folders.session,
            user_id=user.id,
            action="create",
            resource_type="folder",
            resource_id=str(folder.id),
        )
        return folder

    async def update_folder(
        self, user: User, folder_id: uuid.UUID, payload: FolderUpdate
    ) -> Folder:
        folder = await self.get_owned(user, folder_id)

        if payload.parent_id is not None:
            if payload.parent_id == folder.id:
                raise ValidationError("A folder cannot be its own parent.")
            await self.get_owned(user, payload.parent_id)

        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(folder, field, value)

        await self.folders.session.flush()
        await self.folders.session.refresh(folder)
        await record_activity(
            self.folders.session,
            user_id=user.id,
            action="update",
            resource_type="folder",
            resource_id=str(folder.id),
        )
        return folder

    async def delete_folder(self, user: User, folder_id: uuid.UUID) -> None:
        folder = await self.get_owned(user, folder_id)
        await self.folders.soft_delete(folder)
        await record_activity(
            self.folders.session,
            user_id=user.id,
            action="delete",
            resource_type="folder",
            resource_id=str(folder.id),
        )
