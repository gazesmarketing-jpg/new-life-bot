"""Telegram bot entry point for New Life Training Center.

Runs in long-polling mode for local development and testing, and can also
serve a tiny HTTP health endpoint when the PORT environment variable is set
(Render / other PaaS hosts require a listening port to keep the service alive).
A local socket lock prevents two copies from polling the same token.
"""

from __future__ import annotations

import asyncio
import logging
import os
import socket
import sys

from aiogram import Bot, Dispatcher
from aiohttp import web

from app.config import settings
from app.telegram.handlers import setup as telegram_setup

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("newlife.telegram")

# Kept open for the lifetime of the process so a second copy exits early.
_INSTANCE_LOCK: socket.socket | None = None
_LOCK_PORT = 47653


def acquire_instance_lock() -> bool:
    global _INSTANCE_LOCK
    lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock.bind(("127.0.0.1", _LOCK_PORT))
        lock.listen(1)
    except OSError:
        lock.close()
        return False
    _INSTANCE_LOCK = lock
    return True


async def health_handler(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok", "service": "new-life-telegram-bot"})


async def run_health_server(port: int) -> web.AppRunner:
    app = web.Application()
    app.router.add_get("/", health_handler)
    app.router.add_get("/health", health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Health endpoint listening on port %s", port)
    return runner


async def main() -> None:
    if not settings.telegram_token:
        raise RuntimeError("TELEGRAM_TOKEN is not set")
    if not acquire_instance_lock():
        logger.error("Another New Life bot instance is already running; exiting.")
        # Exit code 3 tells start_bot.bat not to restart the watchdog loop.
        raise SystemExit(3)
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()
    telegram_setup.setup(dp)

    port = int(os.getenv("PORT", "0"))
    runner = None
    if port > 0:
        runner = await run_health_server(port)

    logger.info("Starting New Life Telegram bot (polling)")
    try:
        await dp.start_polling(bot)
    finally:
        if runner is not None:
            await runner.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)