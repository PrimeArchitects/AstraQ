"""Read-only audit trail endpoint."""

from fastapi import APIRouter, Depends

from app.api.deps import ActivityLogServiceDep, CurrentUser
from app.schemas.activity_log import ActivityLogResponse
from app.schemas.common import Page, PageParams

router = APIRouter(prefix="/activity-logs", tags=["activity-logs"])


@router.get("", response_model=Page[ActivityLogResponse])
async def list_activity_logs(
    current_user: CurrentUser,
    service: ActivityLogServiceDep,
    page_params: PageParams = Depends(),
) -> Page[ActivityLogResponse]:
    logs, total = await service.list_for_user(
        current_user, page_params.offset, page_params.page_size
    )
    items = [ActivityLogResponse.model_validate(log) for log in logs]
    return page_params.to_page(items, total)
