"""SQLAlchemy ORM models for the New Life Training Center system."""

from app.models.audit_log import AuditLog
from app.models.class_schedule import Class, Schedule
from app.models.document import Document
from app.models.notification import Notification
from app.models.parent import Parent
from app.models.program import Program
from app.models.registration import Registration
from app.models.schedule_assignments import ScheduleAssignment
from app.models.student import Student
from app.models.user import User
from app.models.payment import Payment

__all__ = [
    "AuditLog",
    "Class",
    "Schedule",
    "Document",
    "Notification",
    "Parent",
    "Program",
    "Registration",
    "ScheduleAssignment",
    "Student",
    "User",
    "Payment",
]
