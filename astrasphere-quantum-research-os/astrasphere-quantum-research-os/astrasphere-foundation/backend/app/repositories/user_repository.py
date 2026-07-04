"""User persistence — the only layer allowed to write SQLAlchemy queries for users."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_provider import AuthProvider
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email.lower()))
        return result.scalar_one_or_none()

    async def email_exists(self, email: str) -> bool:
        return await self.get_by_email(email) is not None

    async def create_preferences(self, user_id: uuid.UUID) -> UserPreferences:
        prefs = UserPreferences(user_id=user_id)
        self._session.add(prefs)
        await self._session.flush()
        return prefs

    async def get_preferences(self, user_id: uuid.UUID) -> UserPreferences | None:
        result = await self._session.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def add_auth_provider(
        self, user_id: uuid.UUID, provider: str, provider_account_id: str | None = None
    ) -> AuthProvider:
        link = AuthProvider(
            user_id=user_id, provider=provider, provider_account_id=provider_account_id
        )
        self._session.add(link)
        await self._session.flush()
        return link

    async def get_auth_provider(self, user_id: uuid.UUID, provider: str) -> AuthProvider | None:
        result = await self._session.execute(
            select(AuthProvider).where(
                AuthProvider.user_id == user_id, AuthProvider.provider == provider
            )
        )
        return result.scalar_one_or_none()

    async def list_auth_providers(self, user_id: uuid.UUID) -> list[AuthProvider]:
        result = await self._session.execute(
            select(AuthProvider).where(AuthProvider.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_oauth_account(self, provider: str, provider_account_id: str) -> User | None:
        result = await self._session.execute(
            select(User)
            .join(AuthProvider, AuthProvider.user_id == User.id)
            .where(
                AuthProvider.provider == provider,
                AuthProvider.provider_account_id == provider_account_id,
            )
        )
        return result.scalar_one_or_none()
