"""Chat session/message business logic. No AI calls — persistence only."""

import uuid

from app.core.audit import record_activity
from app.core.exceptions import NotFoundError
from app.models.chat_message import ChatMessage
from app.models.chat_session import ChatSession
from app.models.user import User
from app.repositories.chat_repository import ChatMessageRepository, ChatSessionRepository
from app.repositories.paper_repository import PaperRepository
from app.schemas.chat import ChatMessageCreate, ChatSessionCreate, ChatSessionUpdate
from app.services.base import BaseService


class ChatService(BaseService):
    def __init__(
        self,
        session_repo: ChatSessionRepository,
        message_repo: ChatMessageRepository,
        paper_repo: PaperRepository,
    ) -> None:
        self.sessions = session_repo
        self.messages = message_repo
        self.papers = paper_repo

    async def list_sessions(self, user: User) -> list[ChatSession]:
        return await self.sessions.list_for_owner(user.id)

    async def get_owned(self, user: User, session_id: uuid.UUID) -> ChatSession:
        session = await self.sessions.get_for_owner(session_id, user.id)
        if session is None:
            raise NotFoundError("Chat session not found.")
        return session

    async def create_session(self, user: User, payload: ChatSessionCreate) -> ChatSession:
        if payload.paper_id is not None:
            paper = await self.papers.get_for_owner(payload.paper_id, user.id)
            if paper is None:
                raise NotFoundError("Paper not found.")

        session = ChatSession(owner_id=user.id, title=payload.title, paper_id=payload.paper_id)
        session = await self.sessions.create(session)
        await record_activity(
            self.sessions.session,
            user_id=user.id,
            action="create",
            resource_type="chat_session",
            resource_id=str(session.id),
        )
        return session

    async def update_session(
        self, user: User, session_id: uuid.UUID, payload: ChatSessionUpdate
    ) -> ChatSession:
        session = await self.get_owned(user, session_id)
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(session, field, value)
        await self.sessions.session.flush()
        await self.sessions.session.refresh(session)
        return session

    async def delete_session(self, user: User, session_id: uuid.UUID) -> None:
        session = await self.get_owned(user, session_id)
        await self.sessions.soft_delete(session)
        await record_activity(
            self.sessions.session,
            user_id=user.id,
            action="delete",
            resource_type="chat_session",
            resource_id=str(session_id),
        )

    async def add_message(
        self, user: User, session_id: uuid.UUID, payload: ChatMessageCreate
    ) -> ChatMessage:
        session = await self.get_owned(user, session_id)
        message = ChatMessage(session_id=session.id, role=payload.role, content=payload.content)
        return await self.messages.create(message)
