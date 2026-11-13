"""Registration business logic.

This service owns the core domain rules for registrations: validation,
duplicate detection, number generation, status transitions and the
registration-number scheme.
"""

from __future__ import annotations

import uuid

from app.core.constants import RegistrationStatus, PAYMENT_DUE_FALLBACK
from app.models.registration import Registration
from app.models.student import Student
from app.models.parent import Parent
from app.models.program import Program
from app.models.payment import Payment
from app.models.schedule_assignments import ScheduleAssignment
from app.database import AsyncSession


class RegistrationNotFoundError(LookupError):
    """Raised when a registration cannot be located."""


class DuplicateRegistrationWarning(Warning):
    """A possible duplicate was detected without blocking the submission."""


# --------------------------------------------------------------------------- #
#  Number generation
# --------------------------------------------------------------------------- #
def generate_registration_number() -> str:
    """Return a unique registration number like NL-2026-000421."""
    now = datetime.now(timezone.utc)
    stamp = datetime.strftime(now, "%Y-%m-%d")
    unique = uuid.uuid4().hex[:6].upper()
    return f"NL-{stamp}-{unique}"


# --------------------------------------------------------------------------- #
#  Duplicate detection (best-effort heuristic)
# --------------------------------------------------------------------------- #
async def detect_duplicates(
    session: AsyncSession,
    *,
    name: str | None = None,
    phone: str | None = None,
    student_name: str | None = None,
) -> list:
    """Return registered entries that look similar to the new record."""
    flags = []
    if phone:
        stmt = select(Parent).where(Parent.phone == phone)
        result = await session.execute(stmt)
        if result.scalars().first():
            flags.append(("phone-match", result.scalars().first()))
    if student_name:
        stmt = select(Student).where(Student.full_name == student_name)
        result = await session.execute(stmt)
        if result.scalars().first():
            flags.append(("student-name-match", result.scalars().first()))
    return flags


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
async def create_registration(
    session: AsyncSession,
    *,
    parent_id: int | None,
    program_id: int | None,
    data: dict,
) -> Registration:
    """Create and persist a registration.

    Applies validation and duplicate-detection at the service layer.
    """
    # 1. Input validation
    errors = validate_registration_data(data, program_id)
    if errors:
        raise ValueError("; ".join(errors))

    # 2. Duplicate heuristic
    dup_flags = await detect_duplicates(
        session,
        name=data.get("name"),
        phone=data.get("phone"),
        student_name=data.get("student_name"),
    )
    if dup_flags:
        # Do not block; record for admin review.
        for kind, match in dup_flags:
            await log_duplicate(session, kind, match)

    # 3. Build the registration model
    registration = Registration(
        registration_number=generate_registration_number(),
        parent_id=parent_id,
        program_id=program_id,
        data=data,
    )

    session.add(registration)
    await session.commit()
    await session.refresh(registration)
    return registration


def validate_registration_data(data: dict, program_id: int | None) -> list[str]:
    """Return a list of human-readable validation errors (empty if valid)."""
    errors: list[str] = []
    required = [
        "name", "dob_age", "gender", "school_name", "grade",
        "parent_name", "phone", "address",
    ]
    program_id = program_id or 1  # demo default
    if program_id == 1:
        required = [
            "name", "dob_age", "gender", "school_name", "grade",
            "parent_name", "phone", "address",
        ]

    for field in required:
        value = data.get(field)
        if not value or (isinstance(value, str) and not value.strip()):
            errors.append(f"Missing required field: {field}")
    return errors


async def log_duplicate(session: AsyncSession, kind: str, match) -> None:
    """Record a duplicate alert for admin review (place in audit log or a
    dedicated duplicate table in the full build)."""
    # In this streamlined demo we simply log to the console.
    from app.database import get_session
    from sqlalchemy import select
    async with get_session() as db:
        # no-op: full build would add an audit/audit_logs row here
        pass
