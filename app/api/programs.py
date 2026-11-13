"""Program management endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app import database
from app.core.permissions import Role, has_permission
from app.models.program import Program
from app.api.deps import get_current_roles

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get("", response_model=List[Program])
async def list_programs(
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Program))
        return result.scalars().all()


@router.get("/{program_id}")
async def get_program(program_id: int, current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Program).where(Program.id == program_id)
        result = await session.execute(stmt)
        program = result.scalar_one_or_none()
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
        return program


@router.post("", response_model=Program)
async def create_program(
    payload: dict,
    current_user = Depends(get_current_admin),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        program = Program(
            code=payload.get("code", "prog"),
            name=payload.get("name"),
            description=payload.get("description"),
            eligibility=payload.get("eligibility"),
            duration=payload.get("duration"),
            location=payload.get("location"),
            tuition_fee=payload.get("tuition_fee"),
            schedules_json=payload.get("schedules_json"),
            benefits=payload.get("benefits"),
            sponsorship=payload.get("sponsorship"),
            registration_available=payload.get("registration_available", True),
            demo=payload.get("demo", True),
        )
        session.add(program)
        await session.commit()
        await session.refresh(program)
        return program
