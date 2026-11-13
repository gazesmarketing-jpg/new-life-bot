"""Child registration flow for the Kids Program.

Multi-step wizard with validation, document uploads, goal selection and
summary review.  Progress is stored in FSM and can be resumed later.
"""

from __future__ import annotations

from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import database
from app.telegram import messages, utils

router = Router(name="child_registration")

# --------------------------------------------------------------------------- #
#  Conversation states
# --------------------------------------------------------------------------- #
class ChildRegStates(StatesGroup):
    NAME = "child_name"
    DOB_AGE = "child_dob_age"
    GENDER = "child_gender"
    SCHOOL = "child_school"
    GRADE = "child_grade"
    PARENT_NAME = "child_parent_name"
    PHONE = "child_phone"
    ADDRESS = "child_address"
    PREV_TRAINING = "child_prev_training"
    GOALS = "child_goals"
    DOCUMENTS = "child_documents"
    SCHEDULE = "child_schedule"
    SUMMARY = "child_summary"
    FINAL = "child_final"


# --------------------------------------------------------------------------- #
#  Step helpers
# --------------------------------------------------------------------------- #
_GENDER_TEXTS = {
    "male": "Male",
    "female": "Female",
    "other": "Other / Prefer not to say",
}
_GENDER_CB = {
    "male": "cb_gender_male",
    "female": "cb_gender_female",
    "other": "cb_gender_other",
}

_GOAL_TEXTS = {
    "confidence": "Confidence and self-esteem",
    "communication": "Communication skills",
    "leadership": "Leadership",
    "emotional": "Emotional intelligence",
    "social": "Social skills",
    "critical": "Critical thinking and problem-solving",
    "academic": "Academic performance",
    "time": "Time management",
    "speaking": "Public speaking",
    "responsibility": "Independence and responsibility",
}
_GOAL_CB = {
    "confidence": "cb_goal_confidence",
    "communication": "cb_goal_communication",
    "leadership": "cb_goal_leadership",
    "emotional": "cb_goal_emotional",
    "social": "cb_goal_social",
    "critical": "cb_goal_critical",
    "academic": "cb_goal_academic",
    "time": "cb_goal_time",
    "speaking": "cb_goal_speaking",
    "responsibility": "cb_goal_responsibility",
}


# ------------------------------------------------------------------ #
#  Begin
# ------------------------------------------------------------------ #
async def child_callback(callback: CallbackQuery, state: FSMContext):
    """Route child-registration callbacks."""
    data = callback.data or ""
    lang = (await state.get_data()).get("lang", "english")

    if data == "cb_register_child":
        await callback.answer()
        await callback.message.edit_text(
            messages.t("child_registration:info", lang),
            reply_markup=utils.back_keyboard(),
        )
        await ChildRegStates.NAME.set()
    elif data.startswith("cb_gender_"):
        gender = data.replace("cb_gender_", "")
        await state.update_data(gender=gender)
        await callback.message.edit_text(
            messages.t("child_registration:school", lang),
            reply_markup=utils.back_keyboard(),
        )
        await ChildRegStates.SCHOOL.set()
    elif data.startswith("cb_goal_"):
        goal = data.replace("cb_goal_", "")
        selected = (await state.get_data()).get("goals", [])
        if goal not in selected:
            selected.append(goal)
        await state.update_data(goals=selected)
        # Show a "continue selecting" or "done" choice
        keyboard = [
            [InlineKeyboardButton(text="➕ Add another", callback_data="cb_show_more_goals")],
            [InlineKeyboardButton(text="✅ Done selecting goals", callback_data="cb_goals_done")],
        ]
        await callback.message.edit_text(
            "Select more development goals or mark complete.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        )
    else:
        await callback.answer("Unknown option")


# ------------------------------------------------------------------ #
#  Flow steps
# ------------------------------------------------------------------ #
async def get_child_name(message: Message, state: FSMContext):
    """Step 1: collect the child's full name."""
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(name=value)
    await state.set_state(ChildRegStates.DOB_AGE)
    await message.answer(
        messages.t("child_registration:dob_or_age"),
        reply_markup=utils.back_keyboard(),
    )


async def get_child_dob_age(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(dob_age=value)
    await state.set_state(ChildRegStates.GENDER)
    keyboard = [
        [InlineKeyboardButton(text="👦 Male", callback_data="cb_gender_male")],
        [InlineKeyboardButton(text="👧 Female", callback_data="cb_gender_female")],
        [InlineKeyboardButton(text="🧑 Other", callback_data="cb_gender_other")],
    ]
    await message.answer(
        messages.t("child_registration:gender"),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )


async def get_child_gender(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()
    if text in _GENDER_TEXTS:
        gender = next(k for k, v in _GENDER_TEXTS.items() if v.lower() == text)
        await state.update_data(gender=gender)
        await state.set_state(ChildRegStates.SCHOOL)
        await message.answer(messages.t("child_registration:school"))
    else:
        await message.answer(messages.t("child_registration:validation:missing"))


async def get_child_school(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(school_name=value)
    await state.set_state(ChildRegStates.GRADE)
    await message.answer(messages.t("child_registration:grade"))


async def get_child_grade(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(grade=value)
    await state.set_state(ChildRegStates.PARENT_NAME)
    await message.answer(messages.t("child_registration:parent_name"))


async def get_child_parent_name(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value:
        await message.answer(messages.t("child_registration:validation:missing"))
        return
    await state.update_data(parent_name=value)
    await state.set_state(ChildRegStates.PHONE)
    await message.answer(
        messages.t("child_registration:phone"),
        reply_markup=utils.back_keyboard(),
    )


async def get_child_phone(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    if not value.isdigit() or len(value) < 7:
        await message.answer(messages.t("child_registration:validation:phone"))
        return
    await state.update_data(phone=value)
    await state.set_state(ChildRegStates.ADDRESS)
    await message.answer(
        messages.t("child_registration:address"),
        reply_markup=utils.back_keyboard(),
    )


async def get_child_address(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    await state.update_data(address=value)
    await state.set_state(ChildRegStates.PREV_TRAINING)
    await message.answer(
        messages.t("child_registration:previous_training"),
        reply_markup=utils.back_keyboard(),
    )


async def get_child_prev_training(message: Message, state: FSMContext):
    value = (message.text or "").strip()
    await state.update_data(prev_training=value or "None specified")
    await state.set_state(ChildRegStates.GOALS)
    await message.answer(messages.t("child_registration:goals"))
    # Render the goal picker
    await _render_goals_step(message, state)


async def _render_goals_step(message: Message, state: FSMContext):
    """Render the inline goal selection keyboard."""
    selected = (await state.get_data()).get("goals", [])
    inline_rows = []
    for key, text in _GOAL_TEXTS.items():
        if key in selected:
            label = f"✅ {text}"
        else:
            label = f"⬜ {text}"
        inline_rows.append([InlineKeyboardButton(text=label, callback_data=f"cb_goal_{key}")])
    reply = InlineKeyboardMarkup(inline_keyboard=inline_rows)
    await message.answer("Select development goals:", reply_markup=reply)


async def get_child_goals(message: Message, state: FSMContext):
    """Accept a free-text answer as a fallback but warn complexity."""
    value = (message.text or "").strip()
    await message.answer(
        "Goal entry beyond the list is not supported in this version. "
        "Please use the buttons above.",
        reply_markup=utils.back_keyboard(),
    )


# ------------------------------------------------------------------ #
#  Document upload step
# ------------------------------------------------------------------ #
async def document_step(callback: CallbackQuery, state: FSMContext):
    """Explain documents and offer to upload."""
    await callback.answer()
    await callback.message.edit_text(
        "Upload your required documents (required) or skip optional ones.\n\n"
        "1. Student photograph - required\n"
        "2. Parent/guardian ID - required\n"
        "3. Birth certificate - optional",
        reply_markup=utils.back_keyboard(),
    )


# ------------------------------------------------------------------ #
#  Schedule selection, summary, submission
# ------------------------------------------------------------------ #
async def schedule_step(callback: CallbackQuery, state: FSMContext):
    """Show available schedules (delegated to a service in a full build)."""
    await callback.answer()
    await callback.message.edit_text(
        "Schedule selection will render a list of open classes here. "
        "(See the full build for live schedule data.)",
        reply_markup=utils.back_keyboard(),
    )


async def summary_step(callback: CallbackQuery, state: FSMContext):
    """Display a summary of the collected registration."""
    await callback.answer()
    data = await state.get_data()
    lang = (await state.get_data()).get("lang", "english")
    text = messages.t("confirmation:summary", lang)
    text += f"\n\nChild: {data.get('name')}"
    text += f"\nDOB/Age: {data.get('dob_age')}"
    text += f"\nGender: {data.get('gender')}"
    text += f"\nSchool: {data.get('school_name')}"
    text += f"\nGrade: {data.get('grade')}"
    text += f"\nParent: {data.get('parent_name')}"
    text += f"\nPhone: {data.get('phone')}"
    text += f"\nAddress: {data.get('address')}"
    text += f"\nPrevious training: {data.get('prev_training')}"
    text += f"\nGoals: {', '.join(_GOAL_TEXTS.get(g, g) for g in data.get('goals', [])) or 'None'}"
    text += "\n\nTo submit, confirm. If incorrect, go back and edit."
    await callback.message.answer(
        text,
        reply_markup=utils.confirm_keyboard(lang),
    )


async def final_step(callback: CallbackQuery, state: FSMContext):
    """Persist the registration in the full application."""
    await callback.answer()
    await callback.message.answer(
        messages.t("confirmation:submit"),
        reply_markup=utils.back_keyboard(),
    )
    # In a full build this would call the registration service, generate a
    # registration number, store documents, notify staff, and return a
    # confirmation with a unique registration number.
