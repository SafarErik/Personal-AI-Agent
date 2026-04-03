from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(default="Personal AI Agent", validation_alias="APP_NAME")
    environment: Literal["development", "test", "production"] = Field(
        default="development",
        validation_alias="APP_ENVIRONMENT",
    )
    host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    port: int = Field(default=8000, validation_alias="APP_PORT")

    telegram_bot_token: str = Field(default="", validation_alias="TELEGRAM_BOT_TOKEN")
    telegram_api_base_url: str = Field(
        default="https://api.telegram.org",
        validation_alias="TELEGRAM_API_BASE_URL",
    )
    telegram_polling_enabled: bool = Field(
        default=True,
        validation_alias="TELEGRAM_POLLING_ENABLED",
    )
    telegram_poll_timeout_seconds: int = Field(
        default=10,
        validation_alias="TELEGRAM_POLL_TIMEOUT_SECONDS",
    )
    telegram_poll_interval_seconds: float = Field(
        default=1.0,
        validation_alias="TELEGRAM_POLL_INTERVAL_SECONDS",
    )
    telegram_allowed_chat_ids: Annotated[list[int], NoDecode] = Field(
        default_factory=list,
        validation_alias="TELEGRAM_ALLOWED_CHAT_IDS",
    )

    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="", validation_alias="GEMINI_MODEL")

    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/personal_ai_agent",
        validation_alias="DATABASE_URL",
    )

    @field_validator("telegram_allowed_chat_ids", mode="before")
    @classmethod
    def parse_allowed_chat_ids(cls, value: object) -> list[int]:
        if value in (None, "", []):
            return []

        if isinstance(value, list):
            return [int(item) for item in value]

        return [
            int(item.strip())
            for item in str(value).split(",")
            if item.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
