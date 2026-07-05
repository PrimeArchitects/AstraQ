"""Placeholder team-workspace endpoints. Schema and basic CRUD only —
invites, shared folders, and granular permissions are future work."""

from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps import CurrentUser, TeamServiceDep
from app.schemas.team import (
    TeamMemberCreate,
    TeamMemberResponse,
    TeamWorkspaceCreate,
    TeamWorkspaceResponse,
    TeamWorkspaceUpdate,
)

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=list[TeamWorkspaceResponse])
async def list_workspaces(
    current_user: CurrentUser, service: TeamServiceDep
) -> list[TeamWorkspaceResponse]:
    workspaces = await service.list_workspaces(current_user)
    return [TeamWorkspaceResponse.model_validate(w) for w in workspaces]


@router.post("", response_model=TeamWorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    payload: TeamWorkspaceCreate, current_user: CurrentUser, service: TeamServiceDep
) -> TeamWorkspaceResponse:
    workspace = await service.create_workspace(current_user, payload)
    return TeamWorkspaceResponse.model_validate(workspace)


@router.get("/{workspace_id}", response_model=TeamWorkspaceResponse)
async def get_workspace(
    workspace_id: UUID, current_user: CurrentUser, service: TeamServiceDep
) -> TeamWorkspaceResponse:
    workspace = await service.get_accessible(current_user, workspace_id)
    return TeamWorkspaceResponse.model_validate(workspace)


@router.patch("/{workspace_id}", response_model=TeamWorkspaceResponse)
async def update_workspace(
    workspace_id: UUID,
    payload: TeamWorkspaceUpdate,
    current_user: CurrentUser,
    service: TeamServiceDep,
) -> TeamWorkspaceResponse:
    workspace = await service.update_workspace(current_user, workspace_id, payload)
    return TeamWorkspaceResponse.model_validate(workspace)


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: UUID, current_user: CurrentUser, service: TeamServiceDep
) -> None:
    await service.delete_workspace(current_user, workspace_id)


@router.get("/{workspace_id}/members", response_model=list[TeamMemberResponse])
async def list_members(
    workspace_id: UUID, current_user: CurrentUser, service: TeamServiceDep
) -> list[TeamMemberResponse]:
    members = await service.list_members(current_user, workspace_id)
    return [TeamMemberResponse.model_validate(m) for m in members]


@router.post(
    "/{workspace_id}/members",
    response_model=TeamMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_member(
    workspace_id: UUID,
    payload: TeamMemberCreate,
    current_user: CurrentUser,
    service: TeamServiceDep,
) -> TeamMemberResponse:
    member = await service.add_member(current_user, workspace_id, payload)
    return TeamMemberResponse.model_validate(member)


@router.delete("/{workspace_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    workspace_id: UUID,
    member_id: UUID,
    current_user: CurrentUser,
    service: TeamServiceDep,
) -> None:
    await service.remove_member(current_user, workspace_id, member_id)
