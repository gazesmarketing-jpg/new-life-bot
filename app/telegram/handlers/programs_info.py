"""Program information exploration and section detail handlers."""

from __future__ import annotations

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.telegram import messages, utils

router = Router(name="programs_info")

# --------------------------------------------------------------------------- #
#  Program info screens
# --------------------------------------------------------------------------- #
PROGRAM_INFO = {
    "kids": {
        "title": "Kids Program",
        "title_am": "ትምህርት ሰራተኞች",
        "desc": (
            "The Kids Program focuses on building confidence, social skills, "
            "and emotional intelligence through structured activities, group "
            "games, and guided developmental exercises."
        ),
        "eligibility": "Ages 4-12",
        "duration": "8 weeks (per session)",
        "location": "[Configurable]",
        "tuition_fee": "[Configurable]",
        "benefits": "Safe, structured environment for early development.",
        "sponsorship": "Scholarships available on request.",
        "objectives": (
            "Confidence & self-esteem; Communication skills; Leadership; "
            "Emotional intelligence; Social skills; Critical thinking & "
            "problem-solving; Academic performance; Time management; Public "
            "speaking; Independence & responsibility."
        ),
    },
    "parenting": {
        "title": "Parenting Course",
        "title_am": "የእግዚአብሔር ትምህርት ማስረጃ ተጽዕኖች",
        "desc": (
            "A practical course that gives parents tools for positive "
            "parenting, family communication and everyday parenting "
            "challenges."
        ),
        "eligibility": "Open to all parents and guardians",
        "duration": "6 weeks",
        "location": "[Configurable]",
        "tuition_fee": "[Configurable]",
        "benefits": "Practical tools for everyday parenting challenges.",
        "sponsorship": "Financial aid available for qualifying families.",
        "objectives": "Positive parenting techniques; Family communication; "
                      "Child development knowledge; Stress management; "
                      "Setting boundaries.",
    },
}


def program_section(  # noqa: D401
    callback: CallbackQuery, program_key: str, section: str
):
    """Return the inline keyboard marking the current section."""
    return utils.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                utils.InlineButton("Back", callback_data="cb_program_info"),
            ]
        ]
    )


async def program_callback(callback: CallbackQuery, state: FSMContext):
    """Route program-info callbacks."""
    data = callback.data or ""
    lang = (await state.get_data()).get("lang", "english")

    if data == "cb_program_info":
        await callback.answer()
        await callback.message.edit_text(messages.t("menu:explore_programs", lang))
    elif data.startswith("cb_program_section_"):
        program_key = data.replace("cb_program_section_", "")
        await callback.answer()
        info = PROGRAM_INFO.get(program_key)
        if not info:
            await callback.message.edit_text("No program available.")
            return
        title = info.get("title") or info.get("title_am") or program_key
        text = f"{title}\n\n{info.get('desc', '')}"
        await callback.message.answer(text)
    else:
        await callback.answer("Unknown option")
