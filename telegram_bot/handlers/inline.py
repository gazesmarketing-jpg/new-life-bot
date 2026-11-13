"""Inline keyboard and callback query handlers.

Manages conversation navigation via callback queries, multi-step
conversation state, and the conversation state machine that keeps
user flows consistent across messages.
"""

from __future__ import annotations

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.orm import Session

from telegram_bot.database import get_session
from telegram_bot.models.user import User
from telegram_bot.utils.logging import logger

# ---------------------------------------------------------------------- #
# Callback data namespace constants                                      #
# ---------------------------------------------------------------------- #
CB = {
    "HELP": "nav_help",
    "STATUS": "nav_status",
    "CONFIG": "nav_config",
    "SUBSCRIBE": "action_subscribe",
    "UNSUBSCRIBE": "action_unsubscribe",
}

# ---------------------------------------------------------------------- #
# Command handlers                                                       #
# ---------------------------------------------------------------------- #


async def cb_help(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Here is how to use the bot:\n\n"
        "• /start – Welcome message and navigation.\n"
        "• /help  – This help text.\n"
        "• /status – Current bot status.\n"
        "• /config – Change user settings (admin only for fixes).\n"
        "• /admin  – Admin panel (owner only).\n\n"
        "Use the buttons to navigate.",
        reply_markup=None,
        parse_mode="Markdown",
    )
    await callback.answer()


async def cb_status(callback: CallbackQuery) -> None:
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user: User | None = result.scalar_one_or_none()

    lines = [
        f"👤 User: {callback.from_user.full_name or callback.from_user.username}",
        f"ID: {callback.from_user.id}",
        f"Is admin: {'✅' if user and user.is_admin else '❌'}",
        f"Subscribed: {'✅' if user and user.is_subscribed else '❌'}",
    ]
    status_text = "Bot is running and accepting updates.\n\n" + "\n".join(lines)
    keyboard = [
        [
            {"text": "📊 Status", "callback_data": CB["STATUS"]},
            {"text": "⚙️ Config", "callback_data": CB["CONFIG"]},
            {"text": "📋 Help", "callback_data": CB["HELP"]},
        ]
    ]
    await callback.message.edit_text(
        status_text, reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()


async def cb_config(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Settings page coming soon. Use /config to adjust your settings.",
        reply_markup=None,
        parse_mode="Markdown",
    )
    await callback.answer()


async def cb_subscribe(callback: CallbackQuery) -> None:
    async with get_session() as session:
        await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        # Toggle subscription in a real app and commit.
    keyboard = [
        [
            {"text": "📊 Status", "callback_data": CB["STATUS"]},
            {"text": "⚙️ Config", "callback_data": CB["CONFIG"]},
        ]
    ]
    await callback.message.edit_text(
        "You are now subscribed to updates.",
        reply_markup=keyboard,
    )
    await callback.answer()


async def cb_unsubscribe(callback: CallbackQuery) -> None:
    async with get_session() as session:
        # Unsubscribe and commit in a real app.
        pass
    keyboard = [
        [
            {"text": "📊 Status", "callback_data": CB["STATUS"]},
            {"text": "⚙️ Config", "callback_data": CB["CONFIG"]},
        ]
    ]
    await callback.message.edit_text(
        "You have been unsubscribed from updates.",
        reply_markup=keyboard,
    )
    await callback.answer()


# ---------------------------------------------------------------------- #
# Conversation state machine                                             #
# ---------------------------------------------------------------------- #


async def process_callback(callback: CallbackQuery) -> None:
    """Dispatch a callback query to the right handler based on data."""
    data = callback.data or ""
    if data.startswith("nav_"):
        # Navigation handler.
        await dispatch_callback(callback, data)
    else:
        await callback.answer("Unknown action")


async def dispatch_callback(callback: CallbackQuery, data: str) -> None:
    mapping = {
        CB["HELP"]: cb_help,
        CB["STATUS"]: cb_status,
        CB["CONFIG"]: cb_config,
        CB["SUBSCRIBE"]: cb_subscribe,
        CB["UNSUBSCRIBE"]: cb_unsubscribe,
    }
    handler = mapping.get(data)
    if handler is None:
        await callback.answer("Unknown action")
        return
    await handler(callback)


# ---------------------------------------------------------------------- #
# Dispatcher registration                                                #
# ---------------------------------------------------------------------- #


def setup_callback_handlers(dispatcher: Dispatcher) -> None:
    """Register callback query handlers on *dispatcher*."""
    dispatcher.callback_query.register(cb_help, lambda c: True)
    dispatcher.callback_query.register(cb_status, lambda c: True)
    dispatcher.callback_query.register(cb_config, lambda c: True)
    dispatcher.callback_query.register(cb_subscribe, lambda c: True)
    dispatcher.callback_query.register(cb_unsubscribe, lambda c: True)
