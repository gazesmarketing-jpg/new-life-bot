"""Telegram helper utilities: keyboards, state helpers, validation."""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

MINI_APP_URL = "https://site-b394f5e831a841b3ae810de72fe6f653.freebuff.page/"


def main_menu_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Build the main menu inline keyboard."""
    buttons = [
        [
            InlineKeyboardButton(
                text="📝 Registration",
                web_app=WebAppInfo(url=MINI_APP_URL),
            ),
        ],
        [
            InlineKeyboardButton(text="📚 Explore Programs", callback_data="cb_program_info"),
            InlineKeyboardButton(text="ℹ️ Training Center Info", callback_data="cb_info"),
        ],
        [
            InlineKeyboardButton(text="📋 My Registrations", callback_data="cb_my_registrations"),
            InlineKeyboardButton(text="📞 Contact New Life", callback_data="cb_contact"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def start_keyboard(lang: str = "english") -> ReplyKeyboardMarkup:
    """Build a reply keyboard for the first-run language selection."""
    buttons = [
        [KeyboardButton(text="🇬🇧 English"), KeyboardButton(text="🇪🇹 አማርኛ")],
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard(lang: str = "english") -> InlineKeyboardMarkup:
    """Confirm / go back keyboard for registration summaries."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Confirm", callback_data="cb_confirm_registration"),
                InlineKeyboardButton(text="⬅️ Go Back", callback_data="cb_go_back"),
            ]
        ]
    )


def registration_choice_keyboard() -> InlineKeyboardMarkup:
    """Two registration options shown after the user taps Registration."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧒 Register a Child", callback_data="cb_register_child"),
                InlineKeyboardButton(text="👨‍👩‍👧 Parenting Course", callback_data="cb_register_parenting"),
            ]
        ]
    )


def registration_app_keyboard() -> InlineKeyboardMarkup:
    """Single-button keyboard that opens the registration miniapp.

    Used for old messages that still carry the legacy ``cb_registration``
    callback button.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Open Registration",
                    web_app=WebAppInfo(url=MINI_APP_URL),
                )
            ]
        ]
    )


def back_keyboard() -> InlineKeyboardMarkup:
    """Simple back button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Go Back", callback_data="cb_go_back")]]
    )


def language_change_keyboard() -> InlineKeyboardMarkup:
    """Keyboard to switch language."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇬🇧 English", callback_data="cb_set_lang_english"),
                InlineKeyboardButton(text="🇪🇹 አማርኛ", callback_data="cb_set_lang_amharic"),
            ]
        ]
    )


# Development hint: replace with language-specific button rows when the
# locale dictionary grows.
