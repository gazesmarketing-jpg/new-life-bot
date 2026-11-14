"""Bilingual (Amharic/English) Telegram message templates.

User-facing bot copy lives here so translators and New Life staff can edit it
without touching handler code.  Facts about programs, fees and schedules live
in :mod:`app.telegram.knowledge` — keep this module for the surrounding UI
text only.

Translation glossary (keep these terms consistent across both modules)
---------------------------------------------------------------------------
registration / register   ምዝገባ / መመዝገብ
training session          ክፍለ ጊዜ
batch (of a program)      ቡድን
staff                     ሰራተኞች
main menu                 ዋና ማውጫ
this chat                 ይህ ውይይት
certificate               ሰርተፊኬት
graduation                ምረቃ
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
#  Text content
# --------------------------------------------------------------------------- #
_DATA: dict[str, dict[str, str]] = {
    # --- Welcome / language ------------------------------------------------ #
    "start": {
        "english": (
            "🌟 <b>Welcome to New Life Training and Event Center!</b>\n\n"
            "We help children, parents and teachers grow through life-skills "
            "education, parenting education and professional training.\n\n"
            "Please choose your language."
        ),
        "amharic": (
            "🌟 <b>እንኳን ወደ ኒው ላይፍ ትሬኒንግ ኤንድ ኢቨንት ሴንተር በደህና መጡ!</b>\n\n"
            "ልጆች፣ ወላጆች እና አስተማሪዎች በሕይወት ክህሎት ትምህርት፣ በወላጅነት "
            "ትምህርት እና በሙያ ስልጠና እንዲያድጉ እናገዛለን።\n\n"
            "እባክዎ ቋንቋዎን ይምረጡ።"
        ),
    },
    "lang_select": {
        "english": "Please choose your language.",
        "amharic": "እባክዎ ቋንቋዎን ይምረጡ።",
    },
    "lang_changed": {
        "english": "Language set to English.",
        "amharic": "ቋንቋው ወደ አማርኛ ተቀይሯል።",
    },
    # --- Main menu --------------------------------------------------------- #
    "menu:main": {
        "english": (
            "🏠 <b>Main Menu</b>\n\n"
            "How can we help you today? Choose an option below."
        ),
        "amharic": (
            "🏠 <b>ዋና ማውጫ</b>\n\n"
            "ዛሬ እንዴት ልንረዳዎ እንችላለን? ከታች ካሉት አማራጮች አንዱን ይምረጡ።"
        ),
    },
    "menu:my_registrations": {
        "english": (
            "📋 <b>My Registrations</b>\n\n"
            "You will receive confirmation and updates about your registration "
            "in this chat.\n\n"
            "To check the status of an application, call us at 0970535455 and "
            "tell us the name you registered with."
        ),
        "amharic": (
            "📋 <b>ምዝገባዎቼ</b>\n\n"
            "ስለ ምዝገባዎ ማረጋገጫ እና አዳዲስ መረጃዎች በዚህ ውይይት ይደርስዎታል።\n\n"
            "የምዝገባዎን ሁኔታ ለማወቅ በ0970535455 ይደውሉ እና የተመዘገቡበትን ስም "
            "ይንገሩን።"
        ),
    },
    # --- Registration ------------------------------------------------------ #
    "register:choose": {
        "english": (
            "📝 <b>Registration</b>\n\n"
            "Is this registration for:\n\n"
            "👦 <b>A child</b> — Future Generation Program (ages 8–19)\n"
            "🧑 <b>An adult</b> — Parenting Academy (ages 18+)"
        ),
        "amharic": (
            "📝 <b>ምዝገባ</b>\n\n"
            "ምዝገባው ለማን ነው?\n\n"
            "👦 <b>ለልጅ</b> — የወደፊት ትውልድ ፕሮግራም (8–19 ዓመት)\n"
            "🧑 <b>ለአዋቂ</b> — የወላጅነት አካዳሚ (ከ18 ዓመት በላይ)"
        ),
    },
    "register:form_hint": {
        "english": (
            "Tap the button below to open the registration form. It takes a "
            "few minutes.\n\n"
            "Not sure whether a place is still open? Call us first on "
            "0970535455."
        ),
        "amharic": (
            "የምዝገባ ቅጹን ለመክፈት ከታች ያለውን አዝራር ይጫኑ። ጥቂት ደቂቃዎች ብቻ ይወስዳል።\n\n"
            "ቦታ መኖሩን እርግጠኛ ካልሆኑ መጀመሪያ በ0970535455 ይደውሉ።"
        ),
    },
    # --- Programs ---------------------------------------------------------- #
    "programs:menu": {
        "english": (
            "📚 <b>Our Programs</b>\n\n"
            "Select a program to see the details."
        ),
        "amharic": (
            "📚 <b>ፕሮግራሞቻችን</b>\n\n"
            "ዝርዝር መረጃውን ለማየት ከታች ካሉት ፕሮግራሞች አንዱን ይምረጡ።"
        ),
    },
    # --- Errors / fallback ------------------------------------------------- #
    "error": {
        "english": "Something went wrong. Please try again or call 0970535455.",
        "amharic": "ችግር ተፈጥሯል። እባክዎ እንደገና ይሞክሩ ወይም በ0970535455 ይደውሉ።",
    },
    "error:wrong_lang": {
        "english": "Please choose your language first.",
        "amharic": "እባክዎ መጀመሪያ ቋንቋዎን ይምረጡ።",
    },
}


# --------------------------------------------------------------------------- #
#  Button labels
# --------------------------------------------------------------------------- #
BUTTONS: dict[str, dict[str, str]] = {
    "register": {"english": "📝 Register", "amharic": "📝 ምዝገባ"},
    "programs": {"english": "📚 Programs", "amharic": "📚 ፕሮግራሞች"},
    "about": {"english": "ℹ️ About New Life", "amharic": "ℹ️ ስለ ኒው ላይፍ"},
    "fees": {"english": "💳 Fees", "amharic": "💳 ክፍያ"},
    "faq": {"english": "❓ FAQ", "amharic": "❓ ተደጋጋሚ ጥያቄዎች"},
    "contact": {"english": "📞 Contact & Location", "amharic": "📞 አድራሻ እና ግንኙነት"},
    "my_registrations": {"english": "📋 My Registrations", "amharic": "📋 ምዝገባዎቼ"},
    "language": {"english": "🌐 Language", "amharic": "🌐 ቋንቋ"},
    "register_child": {
        "english": "👦 For my child",
        "amharic": "👦 ለልጄ",
    },
    "register_parenting": {
        "english": "🧑 For myself (adult)",
        "amharic": "🧑 ለራሴ (አዋቂ)",
    },
    "open_form": {
        "english": "📝 Open registration form",
        "amharic": "📝 የምዝገባ ቅጹን ይክፈቱ",
    },
    "back": {"english": "↩ Back", "amharic": "↩ ተመለስ"},
    "main_menu": {"english": "🏠 Main Menu", "amharic": "🏠 ዋና ማውጫ"},
    "english": {"english": "English", "amharic": "English"},
    "amharic": {"english": "አማርኛ", "amharic": "አማርኛ"},
}


def t(key: str, lang: str = "english") -> str:
    """Return the message for *key* in the requested language."""
    entry = _DATA.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("english", key)


def b(key: str, lang: str = "english") -> str:
    """Return the button label for *key* in the requested language."""
    entry = BUTTONS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get("english", key)
