"""Account settings: language switching."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.telegram import messages, utils
from app.telegram.handlers.main_menu import show

router = Router(name="account")


async def account_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Route language-switch callbacks."""
    data = callback.data or ""
    await callback.answer()

    if data == "cb_change_lang":
        await show(callback, messages.t("lang_select"), utils.language_keyboard())
        return

    if data not in {"cb_set_lang_english", "cb_set_lang_amharic"}:
        return

    lang = "english" if data.endswith("english") else "amharic"
    await state.update_data(lang=lang)
    await show(
        callback,
        messages.t("lang_changed", lang) + "\n\n" + messages.t("menu:main", lang),
        utils.main_menu_keyboard(lang),
    )
