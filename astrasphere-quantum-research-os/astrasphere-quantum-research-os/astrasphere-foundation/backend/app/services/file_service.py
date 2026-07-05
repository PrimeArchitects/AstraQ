"""File-metadata business logic. No actual file storage/upload handling —
this only manages the metadata rows described in Prompt 4's scope."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import NotFoundError
from app.models.uploaded_file import UploadedFile
from app.models.user import User
from app.repositories.file_repository import FileRepository
from app.repositories.paper_repository import PaperRepository
from app.schemas.file import UploadedFileCreate, UploadedFileUpdate
from app.services.base import BaseService


class FileService(BaseService):
    def __init__(self, file_repo: FileRepository, paper_repo: PaperRepository) -> None:
        self.files = file_repo
        self.papers = paper_repo

    async def get_owned(self, user: User, file_id: uuid.UUID) -> UploadedFile:
        file = await self.files.get_for_owner(file_id, user.id)
        if file is None:
            raise NotFoundError("File not found.")
        return file

    async def list_files(
        self, user: User, offset: int = 0, limit: int = 20
    ) -> tuple[list[UploadedFile], int]:
        return await self.files.list_paginated_for_owner(user.id, offset, limit)

    async def register_file(self, user: User, payload: UploadedFileCreate) -> UploadedFile:
        if payload.paper_id is not None:
            paper = await self.papers.get_for_owner(payload.paper_id, user.id)
            if paper is None:
                raise NotFoundError("Paper not found.")

        file = UploadedFile(owner_id=user.id, **payload.model_dump())
        file = await self.files.create(file)
        await record_activity(
            self.files.session,
            user_id=user.id,
            action="create",
            resource_type="uploaded_file",
            resource_id=str(file.id),
            extra_data={"filename": file.filename},
        )
        return file

    async def update_file(
        self, user: User, file_id: uuid.UUID, payload: UploadedFileUpdate
    ) -> UploadedFile:
        file = await self.get_owned(user, file_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(file, field, value)
        await self.files.session.flush()
        await self.files.session.refresh(file)
        return file

    async def delete_file(self, user: User, file_id: uuid.UUID) -> None:
        file = await self.get_owned(user, file_id)
        await self.files.soft_delete(file)
        await record_activity(
            self.files.session,
            user_id=user.id,
            action="delete",
            resource_type="uploaded_file",
            resource_id=str(file_id),
        )
