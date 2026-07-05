from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.repositories.base import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatSession)

    async def get_for_owner(self, session_id: UUID, owner_id: UUID) -> ChatSession | None:
        result = await self._session.execute(
            self._base_query()
            .options(selectinload(ChatSession.messages))
            .where(ChatSession.id == session_id, ChatSession.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    async def list_for_owner(self, owner_id: UUID) -> list[ChatSession]:
        result = await self._session.execute(
            self._base_query()
            .where(ChatSession.owner_id == owner_id)
            .order_by(ChatSession.updated_at.desc())
        )
        return list(result.scalars().all())


class ChatMessageRepository(BaseRepository[ChatMessage]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatMessage)
