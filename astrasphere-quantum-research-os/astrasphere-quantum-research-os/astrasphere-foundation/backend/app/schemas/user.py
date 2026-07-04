"""User profile and preferences schemas."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


class UserProfileResponse(ORMModel):
    id: str
    email: str
    display_name: str
    avatar_url: str | None
    bio: str | None
    institution: str | None
    research_interests: list[str]
    timezone: str
    email_verified: bool
    created_at: datetime

    @field_validator("id", mode="before")
    @classmethod
    def coerce_id(cls, v: object) -> str:
        return str(v)


class UserProfileUpdateRequest(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    avatar_url: str | None = Field(default=None, max_length=2048)
    bio: str | None = Field(default=None, max_length=2000)
    institution: str | None = Field(default=None, max_length=255)
    research_interests: list[str] | None = Field(default=None, max_length=25)
    timezone: str | None = Field(default=None, max_length=64)


class UserPreferencesResponse(ORMModel):
    theme: str
    notify_citations: bool
    notify_comments: bool
    notify_weekly_digest: bool


class UserPreferencesUpdateRequest(BaseModel):
    theme: str | None = Field(default=None, pattern="^(light|dark)$")
    notify_citations: bool | None = None
    notify_comments: bool | None = None
    notify_weekly_digest: bool | None = None


class AuthProviderResponse(ORMModel):
    provider: str
    created_at: datetime


class AccountDeleteRequest(BaseModel):
    """Requires re-entering the password (or, for OAuth-only accounts, just confirmation)
    as a deliberate friction point against accidental/CSRF-adjacent deletion."""

    password: str | None = None
    confirm: bool = Field(description="Must be true to proceed.")
