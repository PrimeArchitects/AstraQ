"""Research paper endpoints — pagination, filtering, and sorting live here."""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import CurrentUser, PaperServiceDep
from app.schemas.common import Page, PageParams
from app.schemas.paper import (
    PaperMetadataUpsert,
    ResearchPaperCreate,
    ResearchPaperResponse,
    ResearchPaperUpdate,
)

router = APIRouter(prefix="/papers", tags=["papers"])


@router.get("", response_model=Page[ResearchPaperResponse])
async def list_papers(
    current_user: CurrentUser,
    service: PaperServiceDep,
    page_params: PageParams = Depends(),
    status_filter: str | None = Query(default=None, alias="status"),
    folder_id: UUID | None = None,
    search: str | None = Query(default=None, max_length=200),
    sort_by: Literal["created_at", "updated_at", "title", "year"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
) -> Page[ResearchPaperResponse]:
    papers, total = await service.list_papers(
        current_user,
        offset=page_params.offset,
        limit=page_params.page_size,
        status=status_filter,
        folder_id=folder_id,
        search=search,
        sort_by=sort_by,
        sort_desc=(sort_order == "desc"),
    )
    items = [ResearchPaperResponse.model_validate(p) for p in papers]
    return page_params.to_page(items, total)


@router.post("", response_model=ResearchPaperResponse, status_code=status.HTTP_201_CREATED)
async def create_paper(
    payload: ResearchPaperCreate, current_user: CurrentUser, service: PaperServiceDep
) -> ResearchPaperResponse:
    paper = await service.create_paper(current_user, payload)
    return ResearchPaperResponse.model_validate(paper)


@router.get("/{paper_id}", response_model=ResearchPaperResponse)
async def get_paper(
    paper_id: UUID, current_user: CurrentUser, service: PaperServiceDep
) -> ResearchPaperResponse:
    paper = await service.get_owned(current_user, paper_id)
    return ResearchPaperResponse.model_validate(paper)


@router.patch("/{paper_id}", response_model=ResearchPaperResponse)
async def update_paper(
    paper_id: UUID,
    payload: ResearchPaperUpdate,
    current_user: CurrentUser,
    service: PaperServiceDep,
) -> ResearchPaperResponse:
    paper = await service.update_paper(current_user, paper_id, payload)
    return ResearchPaperResponse.model_validate(paper)


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper(paper_id: UUID, current_user: CurrentUser, service: PaperServiceDep) -> None:
    await service.delete_paper(current_user, paper_id)


@router.put("/{paper_id}/metadata", response_model=ResearchPaperResponse)
async def upsert_paper_metadata(
    paper_id: UUID,
    payload: PaperMetadataUpsert,
    current_user: CurrentUser,
    service: PaperServiceDep,
) -> ResearchPaperResponse:
    paper = await service.upsert_metadata(current_user, paper_id, payload)
    return ResearchPaperResponse.model_validate(paper)
