"""Registration model linking parent, student, and program."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.core.constants import RegistrationStatus


class Registration(Base):
    """A registration submitted by a parent for a child or a course."""

    __tablename__ = "registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    registration_number: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False
    )

    # Parent / guardian link
    parent_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, index=True
    )

    # Student (if Kids Program)
    student_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, index=True
    )

    # Program being registered for
    program_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, index=True
    )

    # Internal fields
    status: Mapped[RegistrationStatus] = mapped_column(
        Enum(RegistrationStatus), default=RegistrationStatus.PENDING_REVIEW
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    def __repr__(self) -> str:
        return f"<Registration(id={self.id}, number={self.registration_number!r}, status={self.status})>"
