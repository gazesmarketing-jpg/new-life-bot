"""Language selection handler."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.telegram import messages, utils
from app.telegram.handlers.main_menu import MenuStates

router = Router(name="language")


async def language_selection(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    if "english" in text or text == "english":
        lang = "english"
    else:
        lang = "amharic"
    await state.update_data(lang=lang)
    await state.set_state(MenuStates.REGISTER_CHILD)
    await message.answer("Language set.", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        messages.t("menu:main", lang),
        reply_markup=utils.main_menu_keyboard(lang),
    )