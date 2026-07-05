"""Tag CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, TagServiceDep
from app.schemas.tag import TagCreate, TagResponse, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse])
async def list_tags(current_user: CurrentUser, service: TagServiceDep) -> list[TagResponse]:
    tags = await service.list_tags(current_user)
    return [TagResponse.model_validate(t) for t in tags]


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    payload: TagCreate, current_user: CurrentUser, service: TagServiceDep
) -> TagResponse:
    tag = await service.create_tag(current_user, payload)
    return TagResponse.model_validate(tag)


@router.patch("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: UUID, payload: TagUpdate, current_user: CurrentUser, service: TagServiceDep
) -> TagResponse:
    tag = await service.update_tag(current_user, tag_id, payload)
    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: UUID, current_user: CurrentUser, service: TagServiceDep) -> None:
    await service.delete_tag(current_user, tag_id)
