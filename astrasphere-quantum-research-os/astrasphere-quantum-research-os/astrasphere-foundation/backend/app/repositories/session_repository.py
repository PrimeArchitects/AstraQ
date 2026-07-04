"""Refresh-token session persistence."""

import hashlib
import uuid
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session
from app.repositories.base import BaseRepository


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()


class SessionRepository(BaseRepository[Session]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Session)

    async def create_session(
        self,
        *,
        session_id: uuid.UUID,
        user_id: uuid.UUID,
        raw_refresh_token: str,
        expires_at: datetime,
        user_agent: str | None,
        ip_address: str | None,
    ) -> Session:
        record = Session(
            id=session_id,
            user_id=user_id,
            refresh_token_hash=hash_refresh_token(raw_refresh_token),
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def get_by_raw_token(self, raw_refresh_token: str) -> Session | None:
        token_hash = hash_refresh_token(raw_refresh_token)
        result = await self._session.execute(
            select(Session).where(Session.refresh_token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke(self, session_record: Session) -> None:
        session_record.revoked_at = datetime.now(UTC)
        await self._session.flush()

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        await self._session.execute(
            update(Session)
            .where(Session.user_id == user_id, Session.revoked_at.is_(None))
            .values(revoked_at=datetime.now(UTC))
        )
        await self._session.flush()

    async def list_active_for_user(self, user_id: uuid.UUID) -> list[Session]:
        result = await self._session.execute(
            select(Session).where(Session.user_id == user_id, Session.revoked_at.is_(None))
        )
        return list(result.scalars().all())
