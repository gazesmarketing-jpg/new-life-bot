"""Main menu, information sections and free-text fallback."""

from __future__ import annotations

import logging

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.telegram import knowledge, messages, utils

logger = logging.getLogger("newlife.telegram.menu")

router = Router(name="main_menu")


class MenuStates(StatesGroup):
    """Conversation states for the bot front-end."""

    SELECT_LANGUAGE = "select_language"


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
async def show(callback: CallbackQuery, text: str, keyboard=None) -> None:
    """Edit the current message, falling back to a new message when needed."""
    try:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    except Exception:  # message too old / unchanged content / not editable
        await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")


async def current_lang(state: FSMContext) -> str:
    return (await state.get_data()).get("lang", "english")


# --------------------------------------------------------------------------- #
#  Commands
# --------------------------------------------------------------------------- #
async def start(message: Message, state: FSMContext) -> None:
    """Entry point: welcome message and language selection."""
    await state.clear()
    await state.set_state(MenuStates.SELECT_LANGUAGE)
    await message.answer(
        messages.t("start", "english") + "\n\n" + messages.t("start", "amharic"),
        reply_markup=utils.start_keyboard(),
        parse_mode="HTML",
    )


async def language_selection(message: Message, state: FSMContext) -> None:
    """Store the chosen language and open the main menu."""
    text = (message.text or "").strip().lower()
    lang = "amharic" if "አማርኛ" in text or "amharic" in text else "english"
    await state.clear()
    await state.update_data(lang=lang)
    await message.answer(
        messages.t("menu:main", lang),
        reply_markup=utils.main_menu_keyboard(lang),
        parse_mode="HTML",
    )


async def free_text(message: Message, state: FSMContext) -> None:
    """Any question we are not sure about goes to staff, never invented."""
    lang = await current_lang(state)
    await message.answer(
        knowledge.pick(knowledge.UNKNOWN_ANSWER, lang),
        reply_markup=utils.main_menu_keyboard(lang),
        parse_mode="HTML",
    )


# --------------------------------------------------------------------------- #
#  Callbacks
# --------------------------------------------------------------------------- #
async def menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Route main-menu and information-section callbacks."""
    data = callback.data or ""
    lang = await current_lang(state)
    await callback.answer()

    if data == "cb_main_menu":
        await show(callback, messages.t("menu:main", lang),
                   utils.main_menu_keyboard(lang))

    elif data == "cb_registration":
        await show(callback, messages.t("register:choose", lang),
                   utils.registration_choice_keyboard(lang))

    elif data == "cb_programs":
        await show(callback, messages.t("programs:menu", lang),
                   utils.programs_keyboard(lang))

    elif data.startswith("cb_program_"):
        key = data.replace("cb_program_", "", 1)
        if key in knowledge.PROGRAMS:
            await show(callback, knowledge.program_card(key, lang),
                       utils.program_keyboard(lang))

    elif data == "cb_about":
        await show(callback, knowledge.ABOUT[lang], utils.back_keyboard(lang))

    elif data == "cb_fees":
        await show(callback, knowledge.FEES[lang], utils.back_keyboard(lang))

    elif data == "cb_faq":
        await show(callback, knowledge.faq_text(lang), utils.back_keyboard(lang))

    elif data == "cb_contact":
        await show(callback, knowledge.CONTACT[lang], utils.back_keyboard(lang))

    elif data == "cb_my_registrations":
        await show(callback, messages.t("menu:my_registrations", lang),
                   utils.back_keyboard(lang))

    elif data == "cb_change_lang":
        await show(callback, messages.t("lang_select", lang),
                   utils.language_keyboard())
