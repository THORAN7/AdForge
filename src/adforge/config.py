"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime settings with safe local defaults."""

    app_name: str = "AdForge"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    llm_provider: str = "template"
    llm_api_key: str | None = None
    llm_model: str | None = None
    allow_external_llm: bool = False
    max_upload_bytes: int = 5 * 1024 * 1024

    model_config = SettingsConfigDict(
        env_prefix="ADFORGE_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings instance."""
    return Settings()

