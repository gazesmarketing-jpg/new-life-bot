"""Schedule assignment model linking approved students to classes."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.core.constants import RegistrationStatus


class ScheduleAssignment(Base):
    """A single student enrolled in a specific class/schedule."""

    __tablename__ = "schedule_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    registration_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, unique=True
    )
    schedule_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    status: Mapped[RegistrationStatus] = mapped_column(
        Enum(RegistrationStatus), default=RegistrationStatus.CLASS_ASSIGNED
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"<ScheduleAssignment(registration_id={self.registration_id}, schedule_id={self.schedule_id})>"
