"""Reports and CSV export endpoints."""

from __future__ import annotations

import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, Response, status

from app import database
from app.core.permissions import Role
from app.models.registration import Registration
from app.models.student import Student
from app.models.payment import Payment
from app.models.class_schedule import Class, Schedule
from app.api.deps import get_current_roles

router = APIRouter(prefix="/reports", tags=["reports"])


def _serializer(reg: Registration) -> dict:
    return {
        "registration_number": reg.registration_number,
        "status": reg.status,
        "submitted_at": reg.submitted_at,
        "parent_name": reg.parent.full_name if reg.parent else "",
        "student_name": reg.student.full_name if reg.student else "",
        "program": reg.program.name if reg.program else "",
        "notes": reg.notes or "",
    }


@router.get("/registrations.csv")
async def export_registrations(
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    """Return registration records as a CSV file."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Registration))
        registrations = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Registration Number", "Status", "Submitted At",
        "Parent Name", "Student Name", "Program", "Notes",
    ])
    for reg in registrations:
        writer.writerow([
            reg.registration_number, reg.status.value,
            reg.submitted_at, reg.parent.full_name if reg.parent else "",
            reg.student.full_name if reg.student else "",
            reg.program.name if reg.program else "",
            reg.notes or "",
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=registrations.csv"},
    )


@router.get("/students.csv")
async def export_students(
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Student))
        students = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student", "Parent", "School", "Grade", "Gender", "DOB/Age"])
    for s in students:
        writer.writerow([
            s.full_name, s.parent_guardian_name, s.school_name,
            s.grade, s.gender, s.date_of_birth or s.age,
        ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"},
    )


@router.get("/classes.csv")
async def export_class_enrollment(
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    """Exports class enrollment data."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        classes_result = await session.execute(select(Class))
        classes = classes_result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Class", "Location", "Capacity", "Enrolled", "Open"])
    for cls in classes:
        for sched in cls.schedules:
            writer.writerow([
                cls.name, cls.location, sched.capacity,
                sched.enrolled_students, sched.is_open,
            ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=class_enrollment.csv"},
    )


@router.get("/payments.csv")
async def export_payments(
    current_user = Depends(get_current_roles(["admin", "finance_officer", "receptionist"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Payment))
        payments = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Registration", "Amount Paid", "Amount Due", "Status", "Due Date"])
    for p in payments:
        writer.writerow([
            p.registration_id, p.amount_paid, p.amount_due,
            p.payment_status.value, p.due_date or "",
        ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=payments.csv"},
    )
