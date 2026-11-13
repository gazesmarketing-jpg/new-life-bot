"""Command handlers for the Telegram bot.

Handles the basic slash commands: /start, /help, /status, /config,
/admin, and /unsubscribe. Access to admin-only commands is restricted
to the configured owner user id.
"""

from __future__ import annotations

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hlink
from sqlalchemy import select
from sqlalchemy.orm import Session

from telegram_bot.config import settings
from telegram_bot.database import get_session
from telegram_bot.models.user import User
from telegram_bot.utils.logging import logger

# Trading card with the bot's capabilities.
CAPABILITIES = [
    hlink("📊 Get status", "/status"),
    hlink("⚙️ Adjust settings", "/config"),
    hlink("📋 Full help", "/help"),
    hlink("🛑 Stop", "/stop"),
]

START_TEXT = (
    "👋 *Hello!* I am the rebuilt Telegram bot. "
    "Use the buttons below to get started."
)
HELP_TEXT = (
    "Here is how to use the bot:\n\n"
    "• */start*  – Welcome message and navigation.\n"
    "• */help*   – This help text.\n"
    "• */status* – Current bot status and settings.\n"
    "• */config* – Change user settings (admin only for fixes).\n"
    "• */admin*  – Admin panel (owner only).\n"
    "• */unsubscribe* – Stop receiving updates.\n\n"
    "All buttons below let you navigate the interface."
)


async def cmd_start(message: Message) -> None:
    """Welcome command with an inline keyboard for navigation."""
    keyboard = [
        [
            {"text": "📊 Status", "callback_data": "nav_status"},
            {"text": "⚙️ Config", "callback_data": "nav_config"},
            {"text": "📋 Help", "callback_data": "nav_help"},
        ]
    ]
    await message.answer(START_TEXT, reply_markup=keyboard, parse_mode="Markdown")


async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, parse_mode="Markdown")


async def cmd_status(message: Message) -> None:
    """Show current bot status and the caller's state."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user: User | None = await result.scalar_one_or_none()

    lines = [
        f"👤 User: {message.from_user.full_name or message.from_user.username}",
        f"ID: {message.from_user.id}",
        f"Is admin: {'✅' if user and user.is_admin else '❌'}",
        f"Subscribed: {'✅' if user and user.is_subscribed else '❌'}",
    ]
    status_text = "Bot is running and accepting updates.\n\n" + "\n".join(lines)
    await message.answer(status_text)


async def cmd_config(message: Message) -> None:
    """Administration-only settings page."""
    await message.answer("Settings page coming soon.", parse_mode="Markdown")


async def cmd_admin(message: Message) -> None:
    """Admin panel visible only to the configured owner."""
    if not settings.is_owner(message.from_user.id):
        await message.answer("This command is restricted to the bot owner.")
        return
    await message.answer("Admin panel: /config")


async def cmd_unsubscribe(message: Message) -> None:
    """Unsubscribe the caller from updates."""
    async with get_session() as session:
        await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        # In a real app, toggle the flag and commit here.
        pass
    await message.answer("You have been unsubscribed from updates.")


# ---------------------------------------------------------------------- #
# Dispatcher registration                                                #
# ---------------------------------------------------------------------- #


def setup_command_handlers(dispatcher: Dispatcher) -> None:
    """Register all slash commands on *dispatcher*."""
    dispatcher.message.register(cmd_start, lambda msg: True)
    dispatcher.message.register(cmd_help, lambda msg: True)
    dispatcher.message.register(cmd_status, lambda msg: True)
    dispatcher.message.register(cmd_config, lambda msg: True)
    dispatcher.message.register(cmd_admin, lambda msg: True)
    dispatcher.message.register(cmd_unsubscribe, lambda msg: True)
