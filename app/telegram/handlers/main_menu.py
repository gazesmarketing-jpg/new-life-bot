"""Main menu and navigation callback handlers."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router(name="main_menu")


class MenuStates(StatesGroup):
    """Conversation states for the bot front-end."""
    SELECT_LANGUAGE = "select_language"
    REGISTER_CHILD = "register_child"
    REGISTER_PARENTING = "register_parenting"
    PROGRAM_INFO = "program_info"
    MY_REGISTRATIONS = "my_registrations"
    CONTACT = "contact"
    ACCOUNT = "account"


from app.telegram import messages, utils


# ------------------------------------------------------------------ #
#  Commands
# ------------------------------------------------------------------ #


async def start(message: Message, state: FSMContext):
    """Entry point: welcome and language selection."""
    lang = getattr(message.from_user, "language_code", None) or "english"
    await state.set_state(MenuStates.SELECT_LANGUAGE)
    await message.answer(
        messages.t("start", lang),
        reply_markup=utils.start_keyboard(),
    )


async def language_selection(message: Message, state: FSMContext):
    """Convert the user's language choice into a state transition."""
    text = message.text or ""
    if "english" in text.lower():
        lang = "english"
    else:
        lang = "amharic"
    await state.update_data(lang=lang)
    await MenuStates.REGISTER_CHILD.set()
    await message.answer(
        messages.t("menu:register_child", lang),
        reply_markup=utils.main_menu_keyboard(lang),
    )


# ------------------------------------------------------------------ #
#  Callback handlers
# ------------------------------------------------------------------ #


async def menu_callback(callback: CallbackQuery, state: FSMContext):
    """Route main-menu callbacks to the right flow."""
    data = callback.data or ""
    lang = (await state.get_data()).get("lang", "english")

    if data == "cb_main_menu":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("menu:main", lang),
            reply_markup=utils.main_menu_keyboard(lang),
        )
    elif data == "cb_registration":
        # Legacy menu buttons: open the registration miniapp as well.
        await callback.answer()
        await callback.message.edit_text(
            "Tap below to open the New Life registration form.",
            reply_markup=utils.registration_app_keyboard(),
        )
    elif data == "cb_program_info":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("programs:kids", lang),
            reply_markup=utils.main_menu_keyboard(lang),
        )
    elif data == "cb_info":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("contact:info", lang),
            reply_markup=utils.main_menu_keyboard(lang),
        )
    elif data == "cb_my_registrations":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("menu:my_registrations", lang),
            reply_markup=utils.main_menu_keyboard(lang),
        )
    elif data == "cb_contact":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("contact:info_text", lang),
            reply_markup=utils.main_menu_keyboard(lang),
        )
    else:
        await callback.answer("Unknown option")
