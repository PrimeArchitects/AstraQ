"""Folder CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, FolderServiceDep
from app.schemas.folder import FolderCreate, FolderResponse, FolderUpdate

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("", response_model=list[FolderResponse])
async def list_folders(
    current_user: CurrentUser, service: FolderServiceDep
) -> list[FolderResponse]:
    folders = await service.list_folders(current_user)
    return [FolderResponse.model_validate(f) for f in folders]


@router.post("", response_model=FolderResponse, status_code=status.HTTP_201_CREATED)
async def create_folder(
    payload: FolderCreate, current_user: CurrentUser, service: FolderServiceDep
) -> FolderResponse:
    folder = await service.create_folder(current_user, payload)
    return FolderResponse.model_validate(folder)


@router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder(
    folder_id: UUID, current_user: CurrentUser, service: FolderServiceDep
) -> FolderResponse:
    folder = await service.get_owned(current_user, folder_id)
    return FolderResponse.model_validate(folder)


@router.patch("/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: UUID, payload: FolderUpdate, current_user: CurrentUser, service: FolderServiceDep
) -> FolderResponse:
    folder = await service.update_folder(current_user, folder_id, payload)
    return FolderResponse.model_validate(folder)


@router.delete("/{folder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_folder(
    folder_id: UUID, current_user: CurrentUser, service: FolderServiceDep
) -> None:
    await service.delete_folder(current_user, folder_id)
