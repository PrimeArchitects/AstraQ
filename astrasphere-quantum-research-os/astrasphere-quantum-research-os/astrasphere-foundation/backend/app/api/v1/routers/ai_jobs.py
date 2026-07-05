"""Placeholder AI job endpoints. Submitting a job only records intent —
no job is actually executed; a future async worker owns that."""

from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps import AIJobServiceDep, CurrentUser
from app.schemas.ai_job import AIJobCreate, AIJobResponse
from app.schemas.common import PageParams

router = APIRouter(prefix="/ai-jobs", tags=["ai-jobs"])


@router.get("", response_model=list[AIJobResponse])
async def list_ai_jobs(
    current_user: CurrentUser,
    service: AIJobServiceDep,
    page_params: PageParams = Depends(),
) -> list[AIJobResponse]:
    jobs = await service.list_for_owner(current_user, page_params.offset, page_params.page_size)
    return [AIJobResponse.model_validate(j) for j in jobs]


@router.post("", response_model=AIJobResponse, status_code=status.HTTP_201_CREATED)
async def submit_ai_job(
    payload: AIJobCreate, current_user: CurrentUser, service: AIJobServiceDep
) -> AIJobResponse:
    job = await service.submit_job(current_user, payload)
    return AIJobResponse.model_validate(job)


@router.get("/{job_id}", response_model=AIJobResponse)
async def get_ai_job(
    job_id: UUID, current_user: CurrentUser, service: AIJobServiceDep
) -> AIJobResponse:
    job = await service.get_owned(current_user, job_id)
    return AIJobResponse.model_validate(job)
