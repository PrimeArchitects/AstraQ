"""File-metadata endpoints. No upload handling — see `UploadedFileCreate`
docstring; this only registers/manages metadata rows."""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import CurrentUser, FileServiceDep
from app.schemas.common import Page, PageParams
from app.schemas.file import UploadedFileCreate, UploadedFileResponse, UploadedFileUpdate

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", response_model=Page[UploadedFileResponse])
async def list_files(
    current_user: CurrentUser,
    service: FileServiceDep,
    page_params: PageParams = Depends(),
) -> Page[UploadedFileResponse]:
    files, total = await service.list_files(current_user, page_params.offset, page_params.page_size)
    items = [UploadedFileResponse.model_validate(f) for f in files]
    return page_params.to_page(items, total)


@router.post("", response_model=UploadedFileResponse, status_code=status.HTTP_201_CREATED)
async def register_file(
    payload: UploadedFileCreate, current_user: CurrentUser, service: FileServiceDep
) -> UploadedFileResponse:
    file = await service.register_file(current_user, payload)
    return UploadedFileResponse.model_validate(file)


@router.get("/{file_id}", response_model=UploadedFileResponse)
async def get_file(
    file_id: UUID, current_user: CurrentUser, service: FileServiceDep
) -> UploadedFileResponse:
    file = await service.get_owned(current_user, file_id)
    return UploadedFileResponse.model_validate(file)


@router.patch("/{file_id}", response_model=UploadedFileResponse)
async def update_file(
    file_id: UUID,
    payload: UploadedFileUpdate,
    current_user: CurrentUser,
    service: FileServiceDep,
) -> UploadedFileResponse:
    file = await service.update_file(current_user, file_id, payload)
    return UploadedFileResponse.model_validate(file)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: UUID, current_user: CurrentUser, service: FileServiceDep) -> None:
    await service.delete_file(current_user, file_id)
