"""Entry point for the Telegram bot.

Runs in polling mode with an in-memory dispatcher. On startup it
registers the command handlers, starts the background scheduler, and
begins listening for updates.

Set ``BOT_TOKEN`` in the environment (or ``.env``) before running.
"""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher

from telegram_bot.config import settings
from telegram_bot.utils.logging import logger
from telegram_bot.handlers import setup_command_handlers, setup_callback_handlers
from telegram_bot.services import Scheduler

# Bot / dispatcher used across the application.
bot: Bot | None = None
dp: Dispatcher | None = None


async def on_startup() -> None:
    """Bootstrap the bot and its services."""
    global bot, dp
    if bot is not None and dp is not None:
        return

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Register all handlers.
    setup_command_handlers(dp)
    setup_callback_handlers(dp)

    # Start the background scheduler.
    scheduler = Scheduler(interval_seconds=settings.scheduler_interval)
    scheduler.start()

    logger.info("Bot started (polling mode) | bot_token_set=%s", bool(settings.bot_token))
    logger.info("Owner user_id=%s", settings.owner_user_id)


async def on_shutdown() -> None:
    """Clean shutdown of the bot."""
    global bot
    if bot is not None:
        await bot.session.close()
        bot = None
    logger.info("Bot shutdown complete")


async def main() -> None:
    """Run the bot indefinitely."""
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception:
        logger.exception("Unhandled exception in main loop")
