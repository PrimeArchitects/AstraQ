"""Notification endpoints (in-app only, no delivery channels)."""

from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, NotificationServiceDep
from app.schemas.common import Page, PageParams
from app.schemas.notification import NotificationMarkReadResponse, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=Page[NotificationResponse])
async def list_notifications(
    current_user: CurrentUser,
    service: NotificationServiceDep,
    page_params: PageParams = Depends(),
) -> Page[NotificationResponse]:
    notifications = await service.list_for_user(
        current_user, page_params.offset, page_params.page_size
    )
    total = await service.total_count(current_user)
    items = [NotificationResponse.model_validate(n) for n in notifications]
    return page_params.to_page(items, total)


@router.get("/unread-count", response_model=NotificationMarkReadResponse)
async def unread_count(
    current_user: CurrentUser, service: NotificationServiceDep
) -> NotificationMarkReadResponse:
    count = await service.unread_count(current_user)
    return NotificationMarkReadResponse(updated=count)


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_read(
    notification_id: UUID, current_user: CurrentUser, service: NotificationServiceDep
) -> NotificationResponse:
    notification = await service.mark_read(current_user, notification_id)
    return NotificationResponse.model_validate(notification)


@router.post("/read-all", response_model=NotificationMarkReadResponse)
async def mark_all_read(
    current_user: CurrentUser, service: NotificationServiceDep
) -> NotificationMarkReadResponse:
    updated = await service.mark_all_read(current_user)
    return NotificationMarkReadResponse(updated=updated)
