"""Student management endpoints."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app import database
from app.core.permissions import Role
from app.models.student import Student
from app.api.deps import get_current_roles

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=List[Student])
async def list_students(
    search: str | None = Query(None),
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Student)
        if search:
            query = query.where(
                Student.full_name.ilike(f"%{search}%")
            )
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/{student_id}")
async def get_student(student_id: int, current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Student).where(Student.id == student_id)
        result = await session.execute(stmt)
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
