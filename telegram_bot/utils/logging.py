"""Logging configuration for the Telegram bot.

Sets up a rotating file logger plus console output so the bot is easy
to monitor in production. Log files live in ``logs/`` and are rotated
automatically.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler

from telegram_bot.config import settings

_LOG_DIR = "logs"
_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
_BACKUP_COUNT = 3


def setup_logging() -> logging.Logger:
    """Configure and return the root logger used by the bot."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Root logger - no propagation so we can control everything.
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler.
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    console.setLevel(level)
    root.addHandler(console)

    # File handler with rotation.
    try:
        import os

        os.makedirs(_LOG_DIR, exist_ok=True)
        file_handler = RotatingFileHandler(
            f"{_LOG_DIR}/bot.log",
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root.addHandler(file_handler)
    except Exception:  # pragma: no cover - file IO is best-effort
        pass

    return root


logger = setup_logging()
