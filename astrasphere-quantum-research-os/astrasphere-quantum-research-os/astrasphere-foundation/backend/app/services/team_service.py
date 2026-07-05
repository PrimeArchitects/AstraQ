"""Placeholder team-workspace business logic. Role permission
enforcement beyond "must be a member" is future work."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.team_member import TeamMember
from app.models.team_workspace import TeamWorkspace
from app.models.user import User
from app.repositories.team_repository import TeamMemberRepository, TeamWorkspaceRepository
from app.schemas.team import TeamMemberCreate, TeamWorkspaceCreate, TeamWorkspaceUpdate
from app.services.base import BaseService


class TeamService(BaseService):
    def __init__(
        self, workspace_repo: TeamWorkspaceRepository, member_repo: TeamMemberRepository
    ) -> None:
        self.workspaces = workspace_repo
        self.members = member_repo

    async def list_workspaces(self, user: User) -> list[TeamWorkspace]:
        return await self.workspaces.list_for_owner(user.id)

    async def get_accessible(self, user: User, workspace_id: uuid.UUID) -> TeamWorkspace:
        workspace = await self.workspaces.get(workspace_id)
        if workspace is None:
            raise NotFoundError("Workspace not found.")
        if workspace.owner_id != user.id:
            membership = await self.members.get_membership(workspace_id, user.id)
            if membership is None:
                raise ForbiddenError("You do not have access to this workspace.")
        return workspace

    async def create_workspace(self, user: User, payload: TeamWorkspaceCreate) -> TeamWorkspace:
        workspace = TeamWorkspace(
            owner_id=user.id, name=payload.name, description=payload.description
        )
        workspace = await self.workspaces.create(workspace)
        await self.members.create(
            TeamMember(workspace_id=workspace.id, user_id=user.id, role="owner")
        )
        await record_activity(
            self.workspaces.session,
            user_id=user.id,
            action="create",
            resource_type="team_workspace",
            resource_id=str(workspace.id),
        )
        return workspace

    async def update_workspace(
        self, user: User, workspace_id: uuid.UUID, payload: TeamWorkspaceUpdate
    ) -> TeamWorkspace:
        workspace = await self.get_accessible(user, workspace_id)
        if workspace.owner_id != user.id:
            raise ForbiddenError("Only the workspace owner can update it.")
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(workspace, field, value)
        await self.workspaces.session.flush()
        await self.workspaces.session.refresh(workspace)
        return workspace

    async def delete_workspace(self, user: User, workspace_id: uuid.UUID) -> None:
        workspace = await self.get_accessible(user, workspace_id)
        if workspace.owner_id != user.id:
            raise ForbiddenError("Only the workspace owner can delete it.")
        await self.workspaces.soft_delete(workspace)
        await record_activity(
            self.workspaces.session,
            user_id=user.id,
            action="delete",
            resource_type="team_workspace",
            resource_id=str(workspace_id),
        )

    async def list_members(self, user: User, workspace_id: uuid.UUID) -> list[TeamMember]:
        await self.get_accessible(user, workspace_id)
        return await self.members.list_for_workspace(workspace_id)

    async def add_member(
        self, user: User, workspace_id: uuid.UUID, payload: TeamMemberCreate
    ) -> TeamMember:
        workspace = await self.get_accessible(user, workspace_id)
        if workspace.owner_id != user.id:
            raise ForbiddenError("Only the workspace owner can add members.")
        if await self.members.get_membership(workspace_id, payload.user_id) is not None:
            from app.core.exceptions import ConflictError

            raise ConflictError("This user is already a member of the workspace.")
        member = TeamMember(workspace_id=workspace_id, user_id=payload.user_id, role=payload.role)
        return await self.members.create(member)

    async def remove_member(
        self, user: User, workspace_id: uuid.UUID, member_id: uuid.UUID
    ) -> None:
        workspace = await self.get_accessible(user, workspace_id)
        if workspace.owner_id != user.id:
            raise ForbiddenError("Only the workspace owner can remove members.")
        member = await self.members.get(member_id)
        if member is None or member.workspace_id != workspace_id:
            raise NotFoundError("Membership not found.")
        await self.members.delete(member)
