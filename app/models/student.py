"""Student / child model for the Kids Program."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Student(Base):
    """Child registered for the Kids Program."""

    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    date_of_birth: Mapped[str | None] = mapped_column(String(32), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender: Mapped[str] = mapped_column(String(32), nullable=False)
    school_name: Mapped[str] = mapped_column(String(128), nullable=False)
    grade: Mapped[str] = mapped_column(String(32), nullable=False)
    parent_guardian_name: Mapped[str] = mapped_column(String(128), nullable=False)
    parent_phone: Mapped[str] = mapped_column(String(32), nullable=False)
    home_address: Mapped[str | None] = mapped_column(String(256), nullable=True)
    previous_training: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(16), default="english")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ------------------------------------------------------------------ #
    #  Relationships
    # ------------------------------------------------------------------ #
    def __repr__(self) -> str:
        return f"<Student(id={self.id}, full_name={self.full_name!r})>"
