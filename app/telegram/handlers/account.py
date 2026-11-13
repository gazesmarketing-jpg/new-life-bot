"""Account settings, language change and profile maintenance."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.telegram import messages, utils

router = Router(name="account")


async def account_callback(callback: CallbackQuery, state: FSMContext):
    """Route account-related callbacks."""
    data = callback.data or ""
    lang = (await state.get_data()).get("lang", "english")

    if data == "cb_settings":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("menu:change_language", lang),
            reply_markup=utils.language_change_keyboard(),
        )
    elif data == "cb_set_lang_english":
        await callback.answer()
        await state.update_data(lang="english")
        await callback.message.edit_text(
            messages.t("menu:register_child", "english"),
            reply_markup=utils.main_menu_keyboard("english"),
        )
    elif data == "cb_set_lang_amharic":
        await callback.answer()
        await state.update_data(lang="amharic")
        await callback.message.edit_text(
            messages.t("menu:register_child", "amharic"),
            reply_markup=utils.main_menu_keyboard("amharic"),
        )
    else:
        await callback.answer("Unknown option")
