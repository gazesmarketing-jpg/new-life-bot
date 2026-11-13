"""Telegram keyboard builders for the New Life bot."""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from app.telegram import knowledge, messages

MINI_APP_URL = knowledge.CENTER["registration_url"]


def _btn(text: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def main_menu_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Main menu: registration first, then information sections."""
    rows = [
        [_btn(messages.b("register", lang), "cb_registration")],
        [
            _btn(messages.b("programs", lang), "cb_programs"),
            _btn(messages.b("about", lang), "cb_about"),
        ],
        [
            _btn(messages.b("fees", lang), "cb_fees"),
            _btn(messages.b("faq", lang), "cb_faq"),
        ],
        [
            _btn(messages.b("contact", lang), "cb_contact"),
            _btn(messages.b("my_registrations", lang), "cb_my_registrations"),
        ],
        [_btn(messages.b("language", lang), "cb_change_lang")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def start_keyboard() -> ReplyKeyboardMarkup:
    """First-run language selection."""
    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="English"),
            KeyboardButton(text="አማርኛ"),
        ]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def language_keyboard() -> InlineKeyboardMarkup:
    """Inline language switcher."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            _btn(messages.b("english"), "cb_set_lang_english"),
            _btn(messages.b("amharic"), "cb_set_lang_amharic"),
        ]]
    )


def registration_choice_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Ask whether the registration is for a child or for an adult."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_btn(messages.b("register_child", lang), "cb_register_child")],
            [_btn(messages.b("register_parenting", lang), "cb_register_parenting")],
            [_btn(messages.b("back", lang), "cb_main_menu")],
        ]
    )


def programs_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """List of the two active programs."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [_btn(knowledge.pick(knowledge.FUTURE_GENERATION["title"], lang),
                  "cb_program_future_generation")],
            [_btn(knowledge.pick(knowledge.PARENTING_ACADEMY["title"], lang),
                  "cb_program_parenting_academy")],
            [_btn(messages.b("main_menu", lang), "cb_main_menu")],
        ]
    )


def program_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Program detail keyboard: open the registration form or go back."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=messages.b("open_form", lang),
                web_app=WebAppInfo(url=MINI_APP_URL),
            )],
            [_btn(messages.b("back", lang), "cb_programs")],
            [_btn(messages.b("main_menu", lang), "cb_main_menu")],
        ]
    )


def back_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Back to the main menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[_btn(messages.b("main_menu", lang), "cb_main_menu")]]
    )
