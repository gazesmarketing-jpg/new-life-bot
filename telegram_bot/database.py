"""Database setup for the Telegram bot.

Uses SQLAlchemy 2.x with a SQLite backend by default. Provides an
engine, a session factory, and declarative base so other modules can
declare models.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from telegram_bot.config import settings

# ``connect_args`` are only meaningful for SQLite.
connect_args: dict[str, dict] = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""

    pass


def get_session():
    """Yield a database session inside a context manager."""
    with SessionLocal() as session:
        yield session
