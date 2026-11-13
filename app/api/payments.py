"""Payment record endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app import database
from app.core.permissions import Role, has_permission
from app.models.payment import Payment
from app.core.constants import PaymentStatus
from app.api.deps import get_current_roles

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("", response_model=List[Payment])
async def list_payments(
    registration_id: int | None = Query(None),
    status: str | None = Query(None, description="Filter by payment status"),
    current_user = Depends(get_current_roles(["admin", "finance_officer", "receptionist"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Payment)
        if registration_id:
            query = query.where(Payment.registration_id == registration_id)
        if status:
            query = query.where(Payment.payment_status == PaymentStatus(status))
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/{payment_id}")
async def get_payment(payment_id: int, current_user = Depends(get_current_roles(["admin", "finance_officer", "receptionist"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await session.execute(stmt)
        payment = result.scalar_one_or_none()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found")
        return payment


@router.patch("/{payment_id}/status", response_model=Payment)
async def update_payment_status(
    payment_id: int,
    payload: dict,
    current_user = Depends(get_current_roles(["admin", "finance_officer", "receptionist"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await session.execute(stmt)
        payment = result.scalar_one_or_none()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found")

        new_status = payload.get("payment_status")
        if new_status:
            payment.payment_status = PaymentStatus(new_status)
            payment.amount_paid = payload.get("amount_paid", payment.amount_paid)

        await session.commit()
        await session.refresh(payment)
        return payment
