"""Parenting Academy registration entry point.

The bot explains the academy and hands the parent over to the official
registration form (Telegram mini app).
"""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.telegram import knowledge, messages, utils
from app.telegram.handlers.main_menu import show

router = Router(name="parenting_course")


async def parenting_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Show the Parenting Academy card with the registration form."""
    lang = (await state.get_data()).get("lang", "english")
    await callback.answer()

    text = (
        knowledge.program_card("parenting_academy", lang)
        + "\n\n"
        + messages.t("register:form_hint", lang)
    )
    await show(callback, text, utils.program_keyboard(lang))
