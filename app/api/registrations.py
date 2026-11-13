"""Registration CRUD endpoints for the staff dashboard."""

from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app import database
from app.core.permissions import Role, has_permission
from app.models.registration import Registration
from app.models.student import Student
from app.models.parent import Parent
from app.models.program import Program
from app.models.class_schedule import Class, Schedule
from app.api.deps import get_current_admin, get_current_roles

router = APIRouter(prefix="/registrations", tags=["registrations"])


# ------------------------------------------------------------------ #
#  List & search
# ------------------------------------------------------------------ #
@router.get("", response_model=List[Registration])
async def list_registrations(
    status: str | None = Query(None, description="Filter by status"),
    search: str | None = Query(None, description="Search by name or phone"),
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Registration)
        if status:
            query = query.where(Registration.status == status)
        if search:
            query = query.where(
                (Registration.data["name"].as_string().ilike(f"%{search}%"))
                | (Registration.data["parent_name"].as_string().ilike(f"%{search}%"))
            )
        result = await session.execute(query)
        return result.scalars().all()


# ------------------------------------------------------------------ #
#  Detail
# ------------------------------------------------------------------ #
@router.get("/{registration_id}", response_model=Registration)
async def get_registration(
    registration_id: int,
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.id == registration_id)
        result = await session.execute(stmt)
        reg = result.scalar_one_or_none()
        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")
        return reg


# ------------------------------------------------------------------ #
#  Status transitions
# ------------------------------------------------------------------ #
@router.patch("/{registration_id}/status", response_model=Registration)
async def update_status(
    registration_id: int,
    payload: dict,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Registration).where(Registration.id == registration_id)
        result = await session.execute(stmt)
        reg = result.scalar_one_or_none()
        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")

        new_status = payload.get("status")
        if new_status and new_status != reg.status:
            # Enforce business rule: no auto-assignment on staff action
            reg.status = new_status
            reg.data["staff_note"] = payload.get("note", reg.data.get("staff_note", ""))
            await session.commit()
            await session.refresh(reg)
        return reg


# ------------------------------------------------------------------ #
#  Class assignment
# ------------------------------------------------------------------ #
@router.post("/{registration_id}/assign-class", response_model=Registration)
async def assign_class(
    registration_id: int,
    payload: dict,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        # Load registration
        stmt = select(Registration).where(Registration.id == registration_id)
        result = await session.execute(stmt)
        reg = result.scalar_one_or_none()
        if not reg:
            raise HTTPException(status_code=404, detail="Registration not found")

        schedule_id = payload.get("schedule_id")
        if not schedule_id:
            raise HTTPException(status_code=400, detail="schedule_id required")

        # Load schedule and check capacity
        schedule_stmt = select(Schedule).where(Schedule.id == schedule_id)
        sched_result = await session.execute(schedule_stmt)
        schedule = sched_result.scalar_one_or_none()
        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        if schedule.enrolled_students >= schedule.capacity:
            raise HTTPException(
                status_code=400,
                detail="Class is full; cannot assign additional students.",
            )

        # Mark the schedule as assigned (capacity accounting)
        schedule.enrolled_students += 1

        # Record assignment
        assignment = ScheduleAssignment(
            registration_id=registration_id,
            schedule_id=schedule_id,
            status=reg.status,
        )
        session.add(assignment)

        # Promote status if needed
        if reg.status == RegistrationStatus.APPROVED:
            reg.status = RegistrationStatus.CLASS_ASSIGNED

        await session.commit()
        await session.refresh(reg)
        await session.refresh(schedule)
        return reg
