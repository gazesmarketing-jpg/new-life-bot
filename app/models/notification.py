"""Notification model for bot/district and dashboard alerts."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.core.constants import NotificationType


class Notification(Base):
    """Logged notification sent to parents or staff."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    notification_type: Mapped[NotificationType] = mapped_column(
        Enum(NotificationType)
    )
    recipient_type: Mapped[str] = mapped_column(String(32), nullable=False)
    recipient_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    subject: Mapped[str] = mapped_column(String(256), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(16), default="english")
    status: Mapped[str] = mapped_column(String(32), default="sent", nullable=False)
    telegram_chat_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    telegram_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.notification_type})>"
