"""Application configuration.

Settings are loaded from environment variables (and an optional `.env` file)
using pydantic-settings. This is the single source of truth for runtime
configuration across the backend.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    environment: str = Field(default="development")
    project_name: str = Field(default="AstraSphere Quantum Research OS")
    log_level: str = Field(default="INFO")

    # API
    api_v1_prefix: str = Field(default="/api/v1")
    secret_key: str = Field(default="change_me_super_secret_key_min_32_chars")
    access_token_expire_minutes: int = Field(default=60)
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    # Postgres
    database_url: str = Field(
        default="postgresql+asyncpg://astrasphere:change_me_dev_password@localhost:5432/astrasphere"
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Qdrant
    qdrant_url: str = Field(default="http://localhost:6333")
    qdrant_collection: str = Field(default="research_documents")

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()


settings = get_settings()
