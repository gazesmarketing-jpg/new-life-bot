"""Child registration entry point (Future Generation Program).

The bot explains the program and hands the parent over to the official
registration form, which runs as a Telegram mini app.  No registration data is
collected or invented inside the chat.
"""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.telegram import knowledge, messages, utils
from app.telegram.handlers.main_menu import show

router = Router(name="child_registration")


async def child_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Show the Future Generation Program card with the registration form."""
    lang = (await state.get_data()).get("lang", "english")
    await callback.answer()

    text = (
        knowledge.program_card("future_generation", lang)
        + "\n\n"
        + messages.t("register:form_hint", lang)
    )
    await show(callback, text, utils.program_keyboard(lang))
