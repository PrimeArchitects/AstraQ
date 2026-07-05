"""Bookmark endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import BookmarkServiceDep, CurrentUser
from app.schemas.bookmark import BookmarkCreate, BookmarkResponse, BookmarkUpdate
from app.schemas.common import Page, PageParams

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.get("", response_model=Page[BookmarkResponse])
async def list_bookmarks(
    current_user: CurrentUser,
    service: BookmarkServiceDep,
    page_params: PageParams = Depends(),
) -> Page[BookmarkResponse]:
    bookmarks, total = await service.list_bookmarks(
        current_user, page_params.offset, page_params.page_size
    )
    items = [BookmarkResponse.model_validate(b) for b in bookmarks]
    return page_params.to_page(items, total)


@router.post("", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    payload: BookmarkCreate, current_user: CurrentUser, service: BookmarkServiceDep
) -> BookmarkResponse:
    bookmark = await service.create_bookmark(current_user, payload)
    return BookmarkResponse.model_validate(bookmark)


@router.patch("/{bookmark_id}", response_model=BookmarkResponse)
async def update_bookmark(
    bookmark_id: UUID,
    payload: BookmarkUpdate,
    current_user: CurrentUser,
    service: BookmarkServiceDep,
) -> BookmarkResponse:
    bookmark = await service.update_bookmark(current_user, bookmark_id, payload)
    return BookmarkResponse.model_validate(bookmark)


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    bookmark_id: UUID, current_user: CurrentUser, service: BookmarkServiceDep
) -> None:
    await service.delete_bookmark(current_user, bookmark_id)
