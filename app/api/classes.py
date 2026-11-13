"""Class and schedule management endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app import database
from app.core.permissions import Role, has_permission
from app.models.class_schedule import Class, Schedule
from app.api.deps import get_current_admin, get_current_roles

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get("", response_model=List[Class])
async def list_classes(
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Class))
        return result.scalars().all()


@router.get("/{class_id}", response_model=Class)
async def get_class(class_id: int, current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Class).where(Class.id == class_id)
        result = await session.execute(stmt)
        cls = result.scalar_one_or_none()
        if not cls:
            raise HTTPException(status_code=404, detail="Class not found")
        return cls


@router.post("", response_model=Class)
async def create_class(
    payload: dict,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        cls = Class(
            name=payload.get("name"),
            description=payload.get("description"),
            location=payload.get("location"),
            is_active=payload.get("is_active", True),
        )
        session.add(cls)
        await session.commit()
        await session.refresh(cls)
        return cls


# ------------------------------------------------------------------ #
#  Schedules
# ------------------------------------------------------------------ #
@router.get("/schedules", response_model=List[Schedule])
async def list_schedules(
    class_id: int | None = Query(None),
    is_open: bool | None = Query(None),
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Schedule)
        if class_id:
            query = query.where(Schedule.class_id == class_id)
        if is_open is not None:
            query = query.where(Schedule.is_open == is_open)
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/schedules/capacity", response_model=List[dict])
async def list_schedules_capacity(
    class_id: int | None = Query(None),
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    """Return schedule capacity info suitable for the parent registration UI."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Schedule)
        if class_id:
            query = query.where(Schedule.class_id == class_id)
        result = await session.execute(query)
        rows = result.scalars().all()
        return [
            {
                "id": s.id,
                "name": f"Class {s.class_id}",
                "day": s.day_of_week,
                "start": s.start_time,
                "end": s.end_time,
                "location": s.location,
                "capacity": s.capacity,
                "enrolled": s.enrolled_students,
                "is_open": s.is_open,
            }
            for s in rows
        ]


@router.post("/{class_id}/schedules", response_model=Schedule)
async def create_schedule(
    class_id: int,
    payload: dict,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        cls_stmt = select(Class).where(Class.id == class_id)
        cls_result = await session.execute(cls_stmt)
        cls = cls_result.scalar_one_or_none()
        if not cls:
            raise HTTPException(status_code=404, detail="Class not found")

        schedule = Schedule(
            class_id=class_id,
            day_of_week=payload.get("day_of_week"),
            start_time=payload.get("start_time"),
            end_time=payload.get("end_time"),
            location=payload.get("location"),
            capacity=payload.get("capacity", 20),
            is_open=payload.get("is_open", True),
        )
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)
        return schedule
