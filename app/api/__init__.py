"""API routers for the staff dashboard."""

from app.api.health import router as health_router
from app.api.registrations import router as registrations_router
from app.api.students import router as students_router
from app.api.programs import router as programs_router
from app.api.classes import router as classes_router
from app.api.documents import router as documents_router
from app.api.payments import router as payments_router
from app.api.reports import router as reports_router
from app.api.notifications import router as notifications_router
from app.api.users import router as users_router

# Aliases for cleaner imports later
health = health_router
registrations = registrations_router
students = students_router
programs = programs_router
classes = classes_router
documents = documents_router
payments = payments_router
reports = reports_router
notifications = notifications_router
users = users_router
