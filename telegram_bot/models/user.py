"""User state model for the Telegram bot.

Tracks per-user conversation state and auxiliary flags so that the bot
can resume multi-step flows reliably across messages.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Integer, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from telegram_bot.database import Base


class User(Base):
    """One row per Telegram user that interacts with the bot."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )
    first_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Free-form JSON blob for arbitrary bot state (inline nav selections,
    # wizard progress, etc.). Kept small and text-backed.
    state: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Simple boolean flags for quick lookups.
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=True)

    # Soft-delete flag so we never lose historical rows.
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Audit timestamps.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<User(telegram_id={self.telegram_id!r}, state={self.state!r})>"
