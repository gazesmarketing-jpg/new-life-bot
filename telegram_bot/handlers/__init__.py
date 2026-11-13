"""Handler registration for the Telegram bot."""

from telegram_bot.handlers.commands import setup_command_handlers
from telegram_bot.handlers.inline import setup_callback_handlers

__all__ = ["setup_command_handlers", "setup_callback_handlers"]
