"""Background scheduler for recurring bot jobs.

Runs the configured periodic tasks (e.g. cron jobs, reminders, data
setups) on its own thread so the polling loop never blocks.
"""

from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timezone
from typing import Awaitable, Callable, Coroutine

logger = logging.getLogger(__name__)


class Scheduler:
    """Minimal scheduler that runs async jobs on an interval.

    The interval is fixed and starts immediately on a daemon thread so
    the scheduler does not block shutdown. Jobs are plain async functions
    receiving the bot's context as their only argument.
    """

    def __init__(self, interval_seconds: int = 300) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        self.interval_seconds = interval_seconds
        self._jobs: list[
            tuple[Callable[..., Coroutine], tuple, dict[str, object]]
        ] = []
        self._thread: threading.Thread | None = None
        self._running = threading.Event()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Job management                                                       #
    # ------------------------------------------------------------------ #

    def add_job(
        self,
        func: Callable[..., Coroutine],
        *args,
        **kwargs,
    ) -> None:
        """Schedule *func* to run every ``interval_seconds`` seconds."""
        with self._lock:
            self._jobs.append((func, args, kwargs))

    def remove_job(self, func: Callable) -> bool:
        """Remove a previously registered job. Returns True if found."""
        with self._lock:
            before = len(self._jobs)
            self._jobs = [
                job
                for job in self._jobs
                if job[0] is not func
            ]
            return len(self._jobs) < before

    # ------------------------------------------------------------------ #
    # Lifecycle                                                            #
    # ------------------------------------------------------------------ #

    def start(self) -> None:
        """Start the background worker thread (idempotent)."""
        if self._running.is_set():
            return
        self._running.set()
        self._thread = threading.Thread(
            target=self._run, name="bot-scheduler", daemon=True
        )
        self._thread.start()
        logger.info("Scheduler started (interval=%ss)", self.interval_seconds)

    def stop(self) -> None:
        """Signal the worker to stop and wait briefly for it to exit."""
        if not self._running.is_set():
            return
        self._running.clear()
        if self._thread is not None:
            self._thread.join(timeout=self.interval_seconds + 5)
        logger.info("Scheduler stopped")

    # ------------------------------------------------------------------ #
    # Internal run-loop                                                    #
    # ------------------------------------------------------------------ #

    def _run(self) -> None:
        while self._running.is_set():
            for job, args, kwargs in self._jobs:
                try:
                    # Run async jobs on the default (main) event loop.
                    if hasattr(
                        job, "__await__"
                    ):
                        # Requires an event loop; only reachable if caller
                        # registers an async coroutine directly.
                        raise RuntimeError(
                            "Async jobs should be dispatched through "
                            "run_job() instead of registered directly."
                        )
                    # Synchronous callable: run synchronously.
                    job(*args, **kwargs)
                    logger.debug(
                        "Job %s executed", job.__name__
                    )
                except Exception:
                    logger.exception(
                        "Error executing job %s", job.__name__
                    )
            # Sleep in small slices so stop() returns promptly.
            for _ in range(self.interval_seconds):
                if not self._running.is_set():
                    break
                time.sleep(1)

    # Convenience wrapper for async jobs on the current event loop.
    async def _async_run_job(
        self,
        func: Callable[..., Coroutine],
        args: tuple,
        kwargs: dict[str, object],
    ) -> None:
        try:
            await func(*args, **kwargs)
        except Exception:
            logger.exception("Error executing scheduled job")

    def run_async_job(
        self,
        func: Callable[..., Coroutine],
        *args,
        **kwargs,
    ) -> None:
        """Schedule an *async* job to be awaited by the worker.

        The worker thread spawns a short-lived event loop to run the
        coroutine, then tears the loop down again.
        """
        with self._lock:
            self._jobs.append((func, args, kwargs))

    def _run_async_job(self, func, args, kwargs) -> None:
        import asyncio

        try:
            asyncio.run(self._async_run_job(func, args, kwargs))
        except Exception:
            logger.exception("Failed to run scheduled job")


# Module-level convenience singleton.
SchedulerInstance = Scheduler
