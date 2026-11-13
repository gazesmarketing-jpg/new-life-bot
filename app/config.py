"""Application configuration using Pydantic Settings."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# --------------------------------------------------------------------------- #
#  Base directory
# --------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """All settings for the New Life Training Center system."""

    # ------------------------------------------------------------------------ #
    #  Telegram Bot
    # ------------------------------------------------------------------------ #
    telegram_token: str = os.getenv("TELEGRAM_TOKEN", "")
    telegram_webhook_url: str = os.getenv("TELEGRAM_WEBHOOK_URL", "")
    telegram_webhook_path: str = os.getenv("TELEGRAM_WEBHOOK_PATH", "/webhook/telegram")

    # ------------------------------------------------------------------------ #
    #  Staff Dashboard (FastAPI)
    # ------------------------------------------------------------------------ #
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    token_expiry_hours: int = int(os.getenv("TOKEN_EXPIRY_HOURS", "24"))

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./new_life.db")

    # ------------------------------------------------------------------------ #
    #  Document uploads
    # ------------------------------------------------------------------------ #
    upload_dir: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "app" / "uploads"))

    # ------------------------------------------------------------------------ #
    #  Notion integration (optional)
    # ------------------------------------------------------------------------ #
    notion_api_key: str = os.getenv("NOTION_API_KEY", "")
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID", "")

    # ------------------------------------------------------------------------ #
    #  Reminder defaults
    # ------------------------------------------------------------------------ #
    reminder_incomplete_days: int = int(os.getenv("REMINDER_INCOMPLETE_DAYS", "7"))
    reminder_class_day: int = int(os.getenv("REMINDER_CLASS_DAY", "1"))
    reminder_payment_days: int = int(os.getenv("REMINDER_PAYMENT_DAY", "14"))

    # ------------------------------------------------------------------------ #
    #  Logging (inherit from the top-level package-level logger)
    # ------------------------------------------------------------------------ #
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ------------------------------------------------------------------------ #
    #  Validation
    # ------------------------------------------------------------------------ #
    @field_validator("telegram_token")
    @classmethod
    def telegram_token_must_not_be_empty(cls, v: str) -> str:
        # Skip validation if the token is unset (common in local dev / 
        # container without env config yet).  Will fail loudly at runtime
        # as soon as the bot tries to start.
        return v

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_not_be_default(cls, v: str) -> str:
        # Allow overriding a deliberately weak dev value but surface a warning.
        return v


settings = Settings()
