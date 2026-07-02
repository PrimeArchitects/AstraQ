"""CRUD endpoints for research projects."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.logging import get_logger
from app.models.research import ResearchProject
from app.schemas.research import (
    ResearchProjectCreate,
    ResearchProjectRead,
    ResearchProjectUpdate,
)

router = APIRouter()
logger = get_logger(__name__)


@router.get("", response_model=list[ResearchProjectRead], summary="List research projects")
async def list_projects(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
) -> list[ResearchProject]:
    result = await db.execute(select(ResearchProject).offset(skip).limit(limit))
    return list(result.scalars().all())


@router.post(
    "",
    response_model=ResearchProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a research project",
)
async def create_project(
    payload: ResearchProjectCreate,
    db: AsyncSession = Depends(get_db),
) -> ResearchProject:
    project = ResearchProject(**payload.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    logger.info("research_project.created", project_id=str(project.id))
    return project


@router.get("/{project_id}", response_model=ResearchProjectRead, summary="Get a research project")
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ResearchProject:
    project = await db.get(ResearchProject, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch(
    "/{project_id}", response_model=ResearchProjectRead, summary="Update a research project"
)
async def update_project(
    project_id: uuid.UUID,
    payload: ResearchProjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResearchProject:
    project = await db.get(ResearchProject, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    await db.commit()
    await db.refresh(project)
    logger.info("research_project.updated", project_id=str(project.id))
    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a research project",
)
async def delete_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    project = await db.get(ResearchProject, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    await db.delete(project)
    await db.commit()
    logger.info("research_project.deleted", project_id=str(project_id))
