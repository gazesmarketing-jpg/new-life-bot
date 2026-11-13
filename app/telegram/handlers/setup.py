"""Register all Telegram command and callback handlers on a Dispatcher."""

from __future__ import annotations

from aiogram import Dispatcher
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State

from app.telegram.handlers import (
    main_menu,
    language,
    child_registration,
    parenting_course,
    programs_info,
    account,
    notifications,
)
from app.telegram.handlers.child_registration import ChildRegStates
from app.telegram.handlers.parenting_course import ParentingRegStates

def setup(dp: Dispatcher):
    """Attach all handlers to *dp*."""
    # --- Command handlers --- #
    dp.message.register(main_menu.start, CommandStart())

    # --- Language selection (reply keyboard) --- #
    dp.message.register(
        language.language_selection,
        StateFilter(main_menu.MenuStates.SELECT_LANGUAGE),
    )

    # --- Child registration message steps --- #
    dp.message.register(
        child_registration.get_child_name,
        StateFilter(ChildRegStates.NAME),
    )
    dp.message.register(
        child_registration.get_child_dob_age,
        StateFilter(ChildRegStates.DOB_AGE),
    )
    dp.message.register(
        child_registration.get_child_school,
        StateFilter(ChildRegStates.SCHOOL),
    )
    dp.message.register(
        child_registration.get_child_grade,
        StateFilter(ChildRegStates.GRADE),
    )
    dp.message.register(
        child_registration.get_child_parent_name,
        StateFilter(ChildRegStates.PARENT_NAME),
    )
    dp.message.register(
        child_registration.get_child_phone,
        StateFilter(ChildRegStates.PHONE),
    )
    dp.message.register(
        child_registration.get_child_address,
        StateFilter(ChildRegStates.ADDRESS),
    )
    dp.message.register(
        child_registration.get_child_prev_training,
        StateFilter(ChildRegStates.PREV_TRAINING),
    )

    # --- Parenting course message steps --- #
    dp.message.register(
        parenting_course.get_pc_name,
        StateFilter(ParentingRegStates.NAME),
    )
    dp.message.register(
        parenting_course.get_pc_phone,
        StateFilter(ParentingRegStates.PHONE),
    )
    dp.message.register(
        parenting_course.get_pc_address,
        StateFilter(ParentingRegStates.ADDRESS),
    )
    dp.message.register(
        parenting_course.get_pc_schedule,
        StateFilter(ParentingRegStates.SCHEDULE),
    )

    # --- Callback query handlers --- #
    dp.callback_query.register(main_menu.menu_callback, lambda c: c.data in {
        "cb_main_menu", "cb_program_info", "cb_info", "cb_my_registrations",
        "cb_contact", "cb_registration",
    })
    dp.callback_query.register(child_registration.child_callback, lambda c: (c.data or "").startswith("cb_register_child") or (c.data or "").startswith("cb_gender_") or (c.data or "").startswith("cb_goal_"))
    dp.callback_query.register(parenting_course.parenting_callback, lambda c: (c.data or "") in {"cb_register_parenting", "cb_confirm_parenting"})
    dp.callback_query.register(programs_info.program_callback, lambda c: (c.data or "") in {"cb_program_info"} or (c.data or "").startswith("cb_program_section_"))
    dp.callback_query.register(account.account_callback, lambda c: (c.data or "").startswith("cb_settings") or (c.data or "").startswith("cb_set_lang_"))
    dp.callback_query.register(notifications.notification_callback, lambda c: (c.data or "").startswith("cb_notifications"))