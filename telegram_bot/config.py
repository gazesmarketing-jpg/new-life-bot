"""Configuration management for the Telegram bot.

All configuration is loaded from environment variables with sensible
defaults. The config is centralized in a single module so every other
component can import a single ``Settings`` object.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- Bot credentials ---
    # Token issued by @BotFather. Must be set in production.
    bot_token: str = os.getenv("BOT_TOKEN", "")

    # --- Auth / ownership ---
    # Telegram user id of the bot owner / admin. Commands that require
    # admin privileges are only accepted from this user id.
    owner_user_id: int = int(os.getenv("OWNER_USER_ID", "0"))

    # --- Database ---
    # URL for the SQLAlchemy database. Defaults to SQLite in the project
    # root. Override for production (e.g. postgresql+psycopg2://...).
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./bot.db")

    # --- Logging ---
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # --- Scheduler ---
    # Interval in seconds between recurring job executions.
    scheduler_interval: int = int(os.getenv("SCHEDULER_INTERVAL", "300"))

    # --- Web server / webhook (optional) ---
    # If set, the bot will run as a webhook instead of polling.
    web_hook_host: str | None = os.getenv("WEBHOOK_HOST")
    web_hook_port: int = int(os.getenv("WEBHOOK_PORT", "8443"))
    web_hook_ssl_cert: str | None = os.getenv("WEBHOOK_SSL_CERT")
    web_hook_ssl_priv: str | None = os.getenv("WEBHOOK_SSL_PRIV")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def is_owner(self, user_id: int) -> bool:
        """Return True if *user_id* matches the configured owner."""
        return user_id == self.owner_user_id


# Singleton used everywhere.
settings: Final[Settings] = Settings()
