"""
Centralized application configuration.

All runtime configuration is sourced from environment variables (via a `.env`
file in local development, or injected directly by the orchestrator in
staging/production). Nothing here should be hardcoded per-environment;
add new settings as typed fields so misconfiguration fails fast at boot
rather than at first use.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    APP_NAME: str = "AstraSphere Quantum Research OS"
    APP_ENV: Literal["local", "test", "staging", "production"] = "local"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False

    # --- Security (placeholders — real auth arrives in a later phase) ---
    SECRET_KEY: str = Field(default="CHANGE_ME_INSECURE_DEV_ONLY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # --- PostgreSQL ---
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "astrasphere"
    POSTGRES_PASSWORD: str = "astrasphere"
    POSTGRES_DB: str = "astrasphere"
    DATABASE_URL: PostgresDsn | None = None

    # --- Redis ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: RedisDsn | None = None

    # --- Qdrant (vector store, for future AI/RAG features) ---
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_PREFIX: str = "astrasphere"

    # --- AI service (placeholder architecture only, no live calls yet) ---
    AI_PROVIDER: Literal["anthropic", "none"] = "none"
    AI_API_KEY: str | None = None
    AI_MODEL: str = "claude-sonnet-5"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str | None, info: ValidationInfo) -> str:
        if v:
            return v
        data = info.data
        return (
            f"postgresql+asyncpg://{data['POSTGRES_USER']}:{data['POSTGRES_PASSWORD']}"
            f"@{data['POSTGRES_HOST']}:{data['POSTGRES_PORT']}/{data['POSTGRES_DB']}"
        )

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_url(cls, v: str | None, info: ValidationInfo) -> str:
        if v:
            return v
        data = info.data
        return f"redis://{data['REDIS_HOST']}:{data['REDIS_PORT']}/{data['REDIS_DB']}"


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton. Import and call this, never instantiate Settings directly."""
    return Settings()
