from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.team_member import TeamMember
from app.models.team_workspace import TeamWorkspace
from app.repositories.base import BaseRepository


class TeamWorkspaceRepository(BaseRepository[TeamWorkspace]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TeamWorkspace)

    async def list_for_owner(self, owner_id: UUID) -> list[TeamWorkspace]:
        result = await self._session.execute(
            self._base_query()
            .where(TeamWorkspace.owner_id == owner_id)
            .order_by(TeamWorkspace.created_at.desc())
        )
        return list(result.scalars().all())


class TeamMemberRepository(BaseRepository[TeamMember]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, TeamMember)

    async def list_for_workspace(self, workspace_id: UUID) -> list[TeamMember]:
        result = await self._session.execute(
            select(TeamMember).where(TeamMember.workspace_id == workspace_id)
        )
        return list(result.scalars().all())

    async def get_membership(self, workspace_id: UUID, user_id: UUID) -> TeamMember | None:
        result = await self._session.execute(
            select(TeamMember).where(
                TeamMember.workspace_id == workspace_id, TeamMember.user_id == user_id
            )
        )
        return result.scalar_one_or_none()
