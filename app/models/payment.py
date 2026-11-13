"""Payment record model for finance tracking."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.core.constants import PaymentStatus, RegistrationStatus


class Payment(Base):
    """Tracks payment status for registrations."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    registration_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    amount_paid: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    amount_due: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), default=PaymentStatus.UNPAID
    )
    method: Mapped[str | None] = mapped_column(String(32), nullable=True)
    transaction_ref: Mapped[str | None] = mapped_column(String(128), nullable=True)
    due_date: Mapped[str | None] = mapped_column(String(32), nullable=True)
    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, registration_id={self.registration_id}, status={self.payment_status})>"
