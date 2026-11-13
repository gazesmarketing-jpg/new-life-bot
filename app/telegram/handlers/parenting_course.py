"""Parenting Course registration flow."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.telegram import messages, utils

router = Router(name="parenting_course")


class ParentingRegStates(StatesGroup):
    NAME = "pc_name"
    PHONE = "pc_phone"
    ADDRESS = "pc_address"
    SCHEDULE = "pc_schedule"
    SUMMARY = "pc_summary"
    FINAL = "pc_final"


# ------------------------------------------------------------------ #
#  Flow steps
# ------------------------------------------------------------------ #
async def parenting_callback(callback: CallbackQuery, state: FSMContext):
    """Route parenting-course callbacks."""
    data = callback.data or ""
    if data == "cb_register_parenting":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("parenting_course:info"),
            reply_markup=utils.back_keyboard(),
        )
        await ParentingRegStates.NAME.set()
    elif data == "cb_confirm_parenting":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("confirmation:submit"),
            reply_markup=utils.back_keyboard(),
        )
    else:
        await callback.answer("Unknown option")


async def get_pc_name(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(name=value)
    await state.set_state(ParentingRegStates.PHONE)
    await message.answer(messages.t("parenting_course:phone"))


async def get_pc_phone(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value.isdigit() or len(value) < 7:
        await message.answer(messages.t("child_registration:validation:phone"))
        return
    await state.update_data(phone=value)
    await state.set_state(ParentingRegStates.ADDRESS)
    await message.answer(messages.t("parenting_course:address"))


async def get_pc_address(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    await state.update_data(address=value)
    await state.set_state(ParentingRegStates.SCHEDULE)
    await message.answer(messages.t("parenting_course:schedule"), reply_markup=utils.back_keyboard())


async def get_pc_schedule(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    await state.update_data(schedule=value or "Not specified")
    await state.set_state(ParentingRegStates.SUMMARY)
    # Show summary
    data = await state.get_data()
    text = messages.t("confirmation:summary")
    text += f"\n\nName: {data.get('name')}\nPhone: {data.get('phone')}\nAddress: {data.get('address')}\nSchedule: {data.get('schedule')}"
    await message.answer(
        text,
        reply_markup=utils.confirm_keyboard(),
    )


async def complete_parenting(callback: CallbackQuery, state: FSMContext):
    """Submit and acknowledge the parenting course registration."""
    await callback.answer()
    await callback.message.edit_text(
        messages.t("confirmation:submit"),
        reply_markup=utils.back_keyboard(),
    )
    # In the full build this would:
    #   - persist the registration
    #   - generate a registration number
    #   - notify staff
    #   - send a confirmation to the parent
    await callback.message.answer(
        "Your Parenting Course registration is complete. "
        "We will email you a confirmation and the next steps. "
        "Thank you.",
        reply_markup=utils.main_menu_keyboard(),
    )
    await state.clear()
