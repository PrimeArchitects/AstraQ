"""User profile, preferences, and account-lifecycle business logic."""

from app.core.exceptions import UnauthorizedError, ValidationError
from app.core.security import verify_password
from app.models.auth_provider import AuthProvider
from app.models.user import User
from app.models.user_preferences import UserPreferences
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserPreferencesUpdateRequest, UserProfileUpdateRequest
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, user_repo: UserRepository, session_repo: SessionRepository) -> None:
        self.users = user_repo
        self.sessions = session_repo

    async def update_profile(self, user: User, updates: UserProfileUpdateRequest) -> User:
        data = updates.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(user, field, value)
        return user

    async def get_preferences(self, user: User) -> UserPreferences:
        prefs = await self.users.get_preferences(user.id)
        if prefs is None:
            # Defensive: every user should get a preferences row at
            # registration/OAuth-linking time, but backfill rather than
            # 500 if one is somehow missing.
            prefs = await self.users.create_preferences(user.id)
        return prefs

    async def update_preferences(
        self, user: User, updates: UserPreferencesUpdateRequest
    ) -> UserPreferences:
        prefs = await self.get_preferences(user)
        data = updates.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(prefs, field, value)
        return prefs

    async def list_auth_providers(self, user: User) -> list[AuthProvider]:
        return await self.users.list_auth_providers(user.id)

    async def delete_account(self, user: User, *, password: str | None, confirm: bool) -> None:
        if not confirm:
            raise ValidationError("Account deletion must be explicitly confirmed.")

        # Password-holding accounts must re-prove identity; OAuth-only
        # accounts (no password set) skip this check since there's
        # nothing to verify against — `confirm=True` is their gate.
        if user.hashed_password is not None:
            if not password or not verify_password(password, user.hashed_password):
                raise UnauthorizedError("Incorrect password.")

        await self.sessions.revoke_all_for_user(user.id)
        await self.users.delete(user)
