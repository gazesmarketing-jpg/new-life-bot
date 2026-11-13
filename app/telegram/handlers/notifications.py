"""Notifications configuration and in-chat alerts."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.telegram import messages, utils

router = Router(name="notifications")


async def notification_callback(callback: CallbackQuery, state: FSMContext):
    """Route notification callbacks."""
    data = callback.data or ""
    lang = (await state.get_data()).get("lang", "english")

    if data == "cb_notifications":
        await callback.answer()
        await callback.message.edit_text(
            "Notifications will arrive here as configured. "
            "Contact the admin to enable a specific channel.",
            reply_markup=utils.back_keyboard(),
        )
    else:
        await callback.answer("Unknown option")
