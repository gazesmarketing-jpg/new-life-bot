"""Notification endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app import database
from app.core.permissions import Role
from app.models.notification import Notification
from app.core.constants import NotificationType
from app.api.deps import get_current_admin, get_current_roles

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=List[Notification])
async def list_notifications(
    type: str | None = Query(None),
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Notification)
        if type:
            query = query.where(Notification.notification_type == NotificationType(type))
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/{notification_id}")
async def get_notification(notification_id: int, current_user = Depends(get_current_admin)):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Notification).where(Notification.id == notification_id)
        result = await session.execute(stmt)
        notif = result.scalar_one_or_none()
        if not notif:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notif
