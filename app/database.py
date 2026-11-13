"""Database setup with SQLAlchemy async engine and session management."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    async_sessionmaker as _async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# Choose SQLite for local dev, PostgreSQL for production.
# SQLite must use the async driver (sqlite+aiosqlite) for async support.
is_sqlite = settings.database_url.startswith("sqlite")
async_url = settings.database_url
if is_sqlite and not async_url.startswith("sqlite+aiosqlite"):
    # Fall back to an in-process async SQLite URL for local dev
    async_url = "sqlite+aiosqlite:///./new_life.db"

_connect_args = (
    {"check_same_thread": False}
    if is_sqlite
    else {"executemany_mode": "values_plus_batch"}
)

_engine = create_async_engine(
    async_url,
    connect_args=_connect_args,
    pool_pre_ping=is_sqlite,
    poolclass=NullPool if is_sqlite else None,
)

AsyncSessionLocal = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)
SessionLocal = sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)


def get_session() -> Generator:
    """Synchronous session for legacy contexts (use AsyncSession for new code)."""
    with SessionLocal() as session:
        yield session


async def get_async_session() -> AsyncSession:
    """Async session dependency for FastAPI routes."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    """Create all tables if they do not exist."""
    from app import models  # noqa: F401
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop all tables (for development/testing only)."""
    from app import models  # noqa: F401
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Alias Base for use in models and migrations.
class Base(DeclarativeBase):
    pass

# Shared for model inheritance.
BaseModel = Base
