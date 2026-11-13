"""Register all Telegram command and callback handlers on a Dispatcher."""

from __future__ import annotations

from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter

from app.telegram.handlers import (
    account,
    child_registration,
    main_menu,
    notifications,
    parenting_course,
)
from app.telegram.handlers.main_menu import MenuStates

# Callbacks owned by the main menu module.
_MENU_CALLBACKS = {
    "cb_main_menu",
    "cb_registration",
    "cb_programs",
    "cb_program_future_generation",
    "cb_program_parenting_academy",
    "cb_about",
    "cb_fees",
    "cb_faq",
    "cb_contact",
    "cb_my_registrations",
    "cb_change_lang",
}


def setup(dp: Dispatcher) -> None:
    """Attach all handlers to *dp*."""
    # --- Commands --- #
    dp.message.register(main_menu.start, CommandStart())
    dp.message.register(main_menu.start, Command("menu"))

    # --- Language selection (reply keyboard) --- #
    dp.message.register(
        main_menu.language_selection,
        StateFilter(MenuStates.SELECT_LANGUAGE),
    )

    # --- Callback queries --- #
    dp.callback_query.register(
        main_menu.menu_callback,
        lambda c: c.data in _MENU_CALLBACKS,
    )
    dp.callback_query.register(
        child_registration.child_callback,
        lambda c: c.data == "cb_register_child",
    )
    dp.callback_query.register(
        parenting_course.parenting_callback,
        lambda c: c.data == "cb_register_parenting",
    )
    dp.callback_query.register(
        account.account_callback,
        lambda c: (c.data or "").startswith("cb_set_lang_"),
    )
    dp.callback_query.register(
        notifications.notification_callback,
        lambda c: (c.data or "").startswith("cb_notifications"),
    )

    # --- Free text: anything not covered goes to staff, never invented --- #
    dp.message.register(main_menu.free_text)
