"""Unit tests for command handlers.

Uses in-memory SQLite database so the command handlers can be exercised
without a live Telegram network connection.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from aiogram.types import Message, User, Chat
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from telegram_bot.config import settings
from telegram_bot.database import Base
from telegram_bot.handlers.commands import (
    cmd_admin,
    cmd_config,
    cmd_start,
    cmd_status,
    cmd_unsubscribe,
)

# Use aiosqlite async driver for in-memory SQLite.
engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)


@pytest.fixture()
async def db_session():
    """Create an in-memory database, create tables, and clean up."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_cmd_start_sends_keyboard():
    message = Message(
        message_id=1,
        date=0,
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Tester", username="tester"),
    )
    with patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer:
        await cmd_start(message)

    assert mock_answer.called
    kwargs = mock_answer.call_args
    assert kwargs.kwargs.get("parse_mode") == "Markdown"


@pytest.mark.asyncio
async def test_cmd_status():
    message = Message(
        message_id=1,
        date=0,
        chat=Chat(id=1, type="private"),
        from_user=User(id=123, is_bot=False, first_name="Tester", username="tester"),
    )
    with (
        patch("telegram_bot.handlers.commands.get_session") as mock_get,
        patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer,
    ):
        mock_session = AsyncMock()
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none = AsyncMock(return_value=None)
        mock_session.execute.return_value = mock_result
        mock_get.return_value.__aenter__.return_value = mock_session
        await cmd_status(message)

        assert mock_session.execute.called
        assert mock_answer.called


@pytest.mark.asyncio
async def test_cmd_admin_not_owner():
    message = Message(
        message_id=1,
        date=0,
        chat=Chat(id=1, type="private"),
        from_user=User(id=999, is_bot=False, first_name="Not", username="owner"),
    )
    with (
        patch("telegram_bot.handlers.commands.settings") as mock_settings,
        patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer,
    ):
        mock_settings.is_owner.return_value = False
        await cmd_admin(message)

        assert "restricted" in mock_answer.call_args.args[0]
        mock_settings.is_owner.assert_called_once_with(999)


@pytest.mark.asyncio
async def test_cmd_unsubscribe():
    message = Message(
        message_id=1,
        date=0,
        chat=Chat(id=1, type="private"),
        from_user=User(id=123, is_bot=False, first_name="Tester", username="tester"),
    )
    with (
        patch("telegram_bot.handlers.commands.get_session") as mock_get,
        patch.object(Message, "answer", new_callable=AsyncMock) as mock_answer,
    ):
        await cmd_unsubscribe(message)

        assert mock_get.called
        assert mock_answer.called
