"""Official New Life Training and Event Center knowledge base.

Every fact the bot states must come from this module.  If a parent asks
something that is not covered here, the bot directs them to staff instead of
guessing (see ``UNKNOWN_ANSWER``).

Sources of truth: the institutional knowledge base document maintained by
New Life management.  Update this file when fees, schedules or batch
information change.
"""

from __future__ import annotations

from typing import Any

# --------------------------------------------------------------------------- #
#  Contact and institutional details
# --------------------------------------------------------------------------- #
CENTER = {
    "name": {
        "english": "New Life Training and Event Center",
        "amharic": "ኒው ላይፍ ትሬኒንግ ኤንድ ኢቨንት ሴንተር",
    },
    "phone": "0970535455",
    "email": "Newlifetecenter@gmail.com",
    "city": {"english": "Addis Ababa, Ethiopia", "amharic": "አዲስ አበባ፣ ኢትዮጵያ"},
    "days": {"english": "Monday – Sunday", "amharic": "ሰኞ – እሁድ"},
    "hours": {"english": "8:00 AM – 6:00 PM", "amharic": "ከጠዋቱ 8:00 – ምሽቱ 6:00"},
    "registration_url": "https://site-b394f5e831a841b3ae810de72fe6f653.freebuff.page/",
    "stats": [
        {"english": "15,000+ students trained", "amharic": "15,000+ የሰለጠኑ ተማሪዎች"},
        {"english": "2,000+ parents trained", "amharic": "2,000+ የሰለጠኑ ወላጆች"},
        {"english": "500+ teachers trained", "amharic": "500+ የሰለጠኑ አስተማሪዎች"},
        {"english": "4 years of experience", "amharic": "የ4 ዓመት ልምድ"},
    ],
}


def pick(value: Any, lang: str = "english") -> str:
    """Return the *lang* variant of a bilingual dict, falling back to English."""
    if isinstance(value, dict):
        return value.get(lang) or value.get("english", "")
    return str(value)


# --------------------------------------------------------------------------- #
#  About
# --------------------------------------------------------------------------- #
ABOUT = {
    "english": (
        "ℹ️ <b>About New Life Training and Event Center</b>\n\n"
        "New Life is an educational and human-development institution in Addis "
        "Ababa that develops the next generation through life-skills education, "
        "parenting education, youth development and professional training.\n\n"
        "We believe education must go beyond academic knowledge. Children and "
        "young people also need confidence, emotional intelligence, "
        "communication, critical thinking, leadership and problem-solving "
        "skills to handle real life. We work with children, parents and "
        "teachers so that families and society feel the impact.\n\n"
        "<b>Our experience</b>\n"
        "• 15,000+ students trained\n"
        "• 2,000+ parents trained\n"
        "• 500+ teachers trained\n"
        "• 4 years of institutional training experience\n\n"
        "<b>Our approach</b>\n"
        "Initial child assessment, life-skills education and practical "
        "learning, psychological support, practical assignments, individual "
        "progress monitoring, and support for parents."
    ),
    "amharic": (
        "ℹ️ <b>ስለ ኒው ላይፍ ትሬኒንግ ኤንድ ኢቨንት ሴንተር</b>\n\n"
        "ኒው ላይፍ በአዲስ አበባ የሚገኝ የትምህርትና የሰው ልማት ተቋም ሲሆን፣ በህይወት ክህሎት "
        "ትምህርት፣ በወላጅነት ትምህርት፣ በወጣት ልማትና በሙያ ስልጠና ትውልዱን ያሳድጋል።\n\n"
        "ትምህርት ከአካዳሚክ እውቀት በላይ መሆን አለበት ብለን እናምናለን። ልጆችና ወጣቶች በራስ "
        "መተማመን፣ ስሜትን መረዳት፣ መግባባት፣ ትችተኝነት፣ አመራርና ችግር መፍታት "
        "ክህሎቶች ይፈልጋሉ። ከልጆች፣ ከወላጆችና ከአስተማሪዎች ጋር በመስራት በቤተሰብና "
        "በህብረተሰብ ላይ ተጽዕኖ እናመጣለን።\n\n"
        "<b>ልምዳችን</b>\n"
        "• 15,000+ ተማሪዎች\n"
        "• 2,000+ ወላጆች\n"
        "• 500+ አስተማሪዎች\n"
        "• የ4 ዓመት የተቋም ስልጠና ልምድ\n\n"
        "<b>አቀራረባችን</b>\n"
        "የመጀመሪያ የልጅ ግምገማ፣ የህይወት ክህሎት ትምህርትና ተግባራዊ ትምህርት፣ "
        "የስነ-ልቦና ድጋፍ፣ ተግባራዊ ስራዎች፣ የግል እድገት ክትትል እና የወላጆች ድጋፍ።"
    ),
}


# --------------------------------------------------------------------------- #
#  Programs
# --------------------------------------------------------------------------- #
FUTURE_GENERATION = {
    "key": "future_generation",
    "title": {
        "english": "🎓 Future Generation Program",
        "amharic": "🎓 የፊውቸር ጄኔሬሽን ፕሮግራም",
    },
    "summary": {
        "english": (
            "Life-skills training for children and teenagers aged 8–19, "
            "preparing them for academic success, personal development, "
            "healthy relationships, leadership and responsible adulthood."
        ),
        "amharic": (
            "ለ8–19 ዓመት ልጆችና ወጣቶች የህይወት ክህሎት ስልጠና፤ ለትምህርት ስኬት፣ "
            "ለግል እድገት፣ ለጤናማ ግንኙነት፣ ለአመራርነትና ለኃላፊነት የሚዘጋጅ።"
        ),
    },
    "facts": {
        "english": [
            ("👥 Age groups", "Group 1: 8–12 years   •   Group 2: 13–19 years"),
            ("⏱ Duration", "8 weeks, 2 sessions per week, 3 hours per session"),
            ("📚 Sessions", "16 sessions in total — 48 training hours"),
            ("💰 Registration fee", "15,000 ETB per child (one-time payment)"),
            (
                "✅ Fee includes",
                "Training sessions, training materials, student workbook, "
                "graduation participation and graduation T-shirt",
            ),
            ("👥 Class size", "Maximum 25 students per class"),
        ],
        "amharic": [
            ("👥 የዕድሜ ቡድኖች", "ቡድን 1፦ 8–12 ዓመት   •   ቡድን 2፦ 13–19 ዓመት"),
            ("⏱ የቆይታ ጊዜ", "8 ሳምንታት፣ በሳምንት 2 ክፍለ ጊዜ፣ አንድ ክፍለ ጊዜ 3 ሰዓት"),
            ("📚 ክፍለ ጊዜዎች", "በአጠቃላይ 16 ክፍለ ጊዜ — 48 የስልጠና ሰዓታት"),
            ("💰 የምዝገባ ክፍያ", "15,000 ብር ለአንድ ልጅ (በአንድ ጊዜ)"),
            (
                "✅ በክፍያው ውስጥ",
                "የስልጠና ክፍለ ጊዜዎች፣ የስልጠና ቁሳቁሶች፣ የተማሪ የስራ ደብተር፣ "
                "በምረቃ ላይ መሳተፍና የምረቃ ቲሸርት",
            ),
            ("👥 የክፍል መጠን", "በአንድ ክፍል ቢበዛ 25 ተማሪዎች"),
        ],
    },
    "topics": {
        "english": [
            "Confidence and self-esteem",
            "Communication skills",
            "Emotional intelligence",
            "Critical thinking",
            "Decision-making",
            "Leadership",
            "Time management",
            "Study skills and academic performance",
            "Financial literacy",
            "Problem-solving",
        ],
        "amharic": [
            "በራስ መተማመንና ራስን ማድነቅ",
            "የመግባቢያ ክህሎት",
            "ስሜትን መረዳትና መቆጣጠር",
            "ትችተኝነት (ክሪቲካል ቲንኪንግ)",
            "ውሳኔ መስጠት",
            "አመራር",
            "ጊዜ ማስተዳደር",
            "የጥናት ክህሎትና የትምህርት አፈጻጸም",
            "የገንዘብ አያያዝ እውቀት",
            "ችግር መፍታት",
        ],
    },
    "extra": {
        "english": (
            "📋 <b>Assessment and development</b>\n"
            "Every child is assessed before training begins — confidence, "
            "communication, emotional intelligence, academic performance, "
            "behaviour and leadership — so we understand each child's "
            "strengths and the areas that need support. Psychological "
            "support, practical assignments and individual progress "
            "monitoring are part of the program.\n\n"
            "🎉 The program ends with an organised graduation.\n\n"
            "ℹ️ Class days and morning/afternoon shifts are fixed for each "
            "batch and differ between batches. We only confirm the schedule "
            "of the batch that is currently open — never invent dates. "
            "Please call us to confirm availability before paying."
        ),
        "amharic": (
            "📋 <b>ግምገማና እድገት</b>\n"
            "ስልጠናው ከመጀመሩ በፊት ለእያንዳንዱ ልጅ ግምገማ ይደረጋል — በራስ መተማመን፣ "
            "መግባባት፣ ስሜትን መረዳት፣ የትምህርት አፈጻጸም፣ ባህሪና አመራርነት — "
            "ጠንካራ ጎኖቹንና ድጋፍ የሚፈልጉ ጎኖቹን ለመለየት። የስነ-ልቦና ድጋፍ፣ "
            "ተግባራዊ ስራዎችና የግል እድገት ክትትል በፕሮግራሙ ውስጥ ይካተታሉ።\n\n"
            "🎉 ፕሮግራሙ በተዘጋጀ የምረቃ ስነ-ስርዓት ይጠናቀቃል።\n\n"
            "ℹ️ የክፍል ቀናትና የጠዋት/ከሰዓት ተራዎች ለእያንዳንዱ ቡድን የተወሰኑ ናቸው። "
            "እኛ የምናረጋግጠው አሁን ለተከፈተው ቡድን መርሐግብር ብቻ ነው። "
            "ከመክፈልዎ በፊት እባክዎ ቦታ መኖሩን ይደውለው ያረጋግጡ።"
        ),
    },
}


PARENTING_ACADEMY = {
    "key": "parenting_academy",
    "title": {
        "english": "👨‍👩‍👧 Parenting Academy",
        "amharic": "👨‍👩‍👧 የወላጅነት አካዳሚ",
    },
    "summary": {
        "english": (
            "For anyone aged 18 or above who wants to understand children and "
            "learn practical parenting skills. You do not need to have a child "
            "enrolled at New Life."
        ),
        "amharic": (
            "ልጆችን መረዳትና ተግባራዊ የወላጅነት ክህሎት ለመማር ለሚፈልግ ከ18 ዓመት በላይ "
            "ለሆነ ማንኛውም ሰው። ልጅዎ በኒው ላይፍ መመዝገቡ አስፈላጊ አይደለም።"
        ),
    },
    "facts": {
        "english": [
            ("💰 Registration fee", "8,000 ETB per parent (one-time)"),
            (
                "📅 Option 1 — Weekday course",
                "Monday to Friday • 9:00 AM – 12:00 PM (3 hours a day) • "
                "3 weeks • 15 sessions • 45 hours",
            ),
            (
                "📅 Option 2 — Weekend course",
                "Saturday and Sunday • 2 hours a day • 6 weeks • 12 sessions • "
                "24 hours",
            ),
            (
                "ℹ️ Important",
                "In the weekend course parents and children attend separate "
                "classes — not the same classroom.",
            ),
            ("🎓 Certificate", "Participants receive a certificate on completion"),
        ],
        "amharic": [
            ("💰 የምዝገባ ክፍያ", "8,000 ብር ለአንድ ወላጅ (በአንድ ጊዜ)"),
            (
                "📅 አማራጭ 1 — የስራ ቀናት ትምህርት",
                "ከሰኞ እስከ አርብ • ከጠዋቱ 9:00 – 12:00 (በቀን 3 ሰዓት) • "
                "3 ሳምንታት • 15 ክፍለ ጊዜ • 45 ሰዓት",
            ),
            (
                "📅 አማራጭ 2 — የሳምንት መጨረሻ ትምህርት",
                "ቅዳሜና እሁድ • በቀን 2 ሰዓት • 6 ሳምንታት • 12 ክፍለ ጊዜ • 24 ሰዓት",
            ),
            (
                "ℹ️ አስፈላጊ ማሳሰቢያ",
                "በሳምንት መጨረሻ ትምህርት ወላጆችና ልጆች በተለያየ ክፍል ይማራሉ — "
                "በአንድ ክፍል አይደለም።",
            ),
            ("🎓 ሰርተፊኬት", "ተሳታፊዎች ትምህርቱን ሲጨርሱ ሰርተፊኬት ያገኛሉ"),
        ],
    },
    "topics": {
        "english": [
            "Understanding children's behaviour",
            "Raising confident children",
            "Positive discipline",
            "Parent–child communication",
            "Supporting academic performance",
            "Child psychology and development",
            "Technology and screen-time management",
        ],
        "amharic": [
            "የልጆችን ባህሪ መረዳት",
            "በራስ የሚተማመኑ ልጆችን ማሳደግ",
            "አዎንታዊ ተግሣጽ",
            "በወላጅና በልጅ መካከል ግንኙነት",
            "የትምህርት አፈጻጸምን መደገፍ",
            "የልጆች ስነ-ልቦናና እድገት",
            "ቴክኖሎጂ እና የስክሪን ጊዜ አስተዳደር",
        ],
    },
    "extra": {
        "english": (
            "ℹ️ Registration depends on the batch that is currently "
            "announced. Please call us to confirm which formats are open."
        ),
        "amharic": (
            "ℹ️ ምዝገባው አሁን በተከፈተው ቡድን ላይ የተመሰረተ ነው። የትኞቹ አማራጮች "
            "እንደተከፈቱ ለማወቅ እባክዎ ይደውሉልን።"
        ),
    },
}

PROGRAMS = {
    "future_generation": FUTURE_GENERATION,
    "parenting_academy": PARENTING_ACADEMY,
}


def program_card(key: str, lang: str = "english") -> str:
    """Render a full program card as HTML-formatted Telegram text."""
    program = PROGRAMS[key]
    lines = [f"<b>{pick(program['title'], lang)}</b>", "", pick(program["summary"], lang), ""]

    for label, value in program["facts"][lang]:
        lines.append(f"<b>{label}</b>\n{value}")

    topics = program["topics"][lang]
    lines.append("")
    lines.append("<b>" + ("📖 What you learn" if lang == "english" else "📖 የሚማሩት") + "</b>")
    for index, topic in enumerate(topics, start=1):
        lines.append(f"{index}. {topic}")

    lines.append("")
    lines.append(program["extra"][lang])
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
#  Fees and payment
# --------------------------------------------------------------------------- #
FEES = {
    "english": (
        "💳 <b>Fees and payment</b>\n\n"
        "🎓 <b>Future Generation Program</b> — 15,000 ETB per child\n"
        "👨‍👩‍👧 <b>Parenting Academy</b> — 8,000 ETB per parent\n\n"
        "<b>How payment works</b>\n"
        "• Payment is made once — there are no monthly instalments.\n"
        "• Payment is by bank transfer using New Life's official account "
        "details.\n"
        "• Bank details are never sent by this chat. Ask staff for the "
        "official account or get them from New Life directly.\n"
        "• Confirm that a place is available before you pay.\n"
        "• Each class has a maximum of 25 students, so places are limited.\n\n"
        "☎️ 0970535455   ✉️ Newlifetecenter@gmail.com"
    ),
    "amharic": (
        "💳 <b>ክፍያ</b>\n\n"
        "🎓 <b>የፊውቸር ጄኔሬሽን ፕሮግራም</b> — 15,000 ብር ለአንድ ልጅ\n"
        "👨‍👩‍👧 <b>የወላጅነት አካዳሚ</b> — 8,000 ብር ለአንድ ወላጅ\n\n"
        "<b>የክፍያ ሂደት</b>\n"
        "• ክፍያ በአንድ ጊዜ ነው — ወርሃዊ ክፍያ የለም።\n"
        "• ክፍያ የሚፈጸመው በባንክ ዝውውር በኒው ላይፍ ኦፊሴላዊ የሂሳብ ቁጥር ነው።\n"
        "• የባንክ ሂሳብ ቁጥር በዚህ ቻት አይላክም። ኦፊሴላዊውን የሂሳብ ቁጥር "
        "ከሰራተኞቻችን ይጠይቁ።\n"
        "• ከመክፈልዎ በፊት ቦታ መኖሩን ያረጋግጡ።\n"
        "• በአንድ ክፍል ቢበዛ 25 ተማሪዎች ብቻ ስለሆኑ ቦታ የተወሰነ ነው።\n\n"
        "☎️ 0970535455   ✉️ Newlifetecenter@gmail.com"
    ),
}


# --------------------------------------------------------------------------- #
#  Contact
# --------------------------------------------------------------------------- #
CONTACT = {
    "english": (
        "📞 <b>Contact and location</b>\n\n"
        "📍 Addis Ababa, Ethiopia\n"
        "🕗 Monday – Sunday, 8:00 AM – 6:00 PM\n"
        "☎️ 0970535455\n"
        "✉️ Newlifetecenter@gmail.com\n\n"
        "You are welcome to visit the center before registering. Call us for "
        "the exact address and directions.\n\n"
        "Our team speaks Amharic and English."
    ),
    "amharic": (
        "📞 <b>አድራሻና ግንኙነት</b>\n\n"
        "📍 አዲስ አበባ፣ ኢትዮጵያ\n"
        "🕗 ሰኞ – እሁድ፣ ከጠዋቱ 8:00 – ምሽቱ 6:00\n"
        "☎️ 0970535455\n"
        "✉️ Newlifetecenter@gmail.com\n\n"
        "ከመመዝገብዎ በፊት ማዕከሉን መጎብኘት ይችላሉ። ትክክለኛ አድራሻና "
        "አቅጣጫ ለማግኘት ይደውሉልን።\n\n"
        "ቡድናችን በአማርኛና በእንግሊዝኛ ያገለግላል።"
    ),
}


# --------------------------------------------------------------------------- #
#  Frequently asked questions
# --------------------------------------------------------------------------- #
FAQ: list[tuple[dict[str, str], dict[str, str]]] = [
    (
        {"english": "What ages can join the Future Generation Program?",
         "amharic": "የፊውቸር ጄኔሬሽን ፕሮግራምን የሚቀላቀሉ ዕድሜዎች ስንት ናቸው?"},
        {"english": "Children aged 8–19. Group 1 is 8–12 and Group 2 is 13–19.",
         "amharic": "ከ8–19 ዓመት ልጆች። ቡድን 1 ከ8–12፣ ቡድን 2 ከ13–19 ዓመት ነው።"},
    ),
    (
        {"english": "How long does the Future Generation Program take?",
         "amharic": "የፊውቸር ጄኔሬሽን ፕሮግራም ምን ያህል ጊዜ ይወስዳል?"},
        {"english": "8 weeks, two sessions a week, 3 hours per session — "
                    "16 sessions and 48 hours in total.",
         "amharic": "8 ሳምንታት፣ በሳምንት ሁለት ክፍለ ጊዜ፣ አንድ ክፍለ ጊዜ 3 ሰዓት — "
                    "በአጠቃላይ 16 ክፍለ ጊዜና 48 ሰዓት።"},
    ),
    (
        {"english": "How much does it cost?", "amharic": "ክፍያው ስንት ነው?"},
        {"english": "Future Generation Program: 15,000 ETB per child. "
                    "Parenting Academy: 8,000 ETB per parent. Both are paid once.",
         "amharic": "የፊውቸር ጄኔሬሽን ፕሮግራም፦ 15,000 ብር ለአንድ ልጅ። "
                    "የወላጅነት አካዳሚ፦ 8,000 ብር ለአንድ ወላጅ። ሁለቱም በአንድ ጊዜ ናቸው።"},
    ),
    (
        {"english": "Can I choose my child's training days?",
         "amharic": "የልጄን የስልጠና ቀናት መምረጥ እችላለሁ?"},
        {"english": "Class days are fixed for each batch. Morning or afternoon "
                    "options depend on the announced batch, so please confirm "
                    "with staff.",
         "amharic": "የክፍል ቀናት ለእያንዳንዱ ቡድን ተወስነዋል። የጠዋት ወይም የከሰዓት አማራጭ "
                    "በተከፈተው ቡድን ይወሰናል፤ እባክዎ ከሰራተኞቻችን ያረጋግጡ።"},
    ),
    (
        {"english": "When can I register?", "amharic": "መቼ መመዝገብ እችላለሁ?"},
        {"english": "Registration opens when New Life announces a new batch. "
                    "Call us to check whether registration is currently open.",
         "amharic": "ኒው ላይፍ አዲስ ቡድን ሲያስታውቅ ምዝገባ ይከፈታል። ምዝገባ አሁን "
                    "እንደተከፈተ ለማወቅ ይደውሉልን።"},
    ),
    (
        {"english": "Can I visit the center before registering?",
         "amharic": "ከመመዝገብ በፊት ማዕከሉን መጎብኘት እችላለሁ?"},
        {"english": "Yes. The center is open every day from 8:00 AM to 6:00 PM.",
         "amharic": "አዎ። ማዕከሉ በየቀኑ ከጠዋቱ 8:00 እስከ ምሽቱ 6:00 ክፍት ነው።"},
    ),
    (
        {"english": "Does New Life assess children?",
         "amharic": "ኒው ላይፍ ልጆችን ይገምግማል?"},
        {"english": "Yes. An initial assessment identifies each child's "
                    "strengths and the areas that need support.",
         "amharic": "አዎ። የመጀመሪያ ግምገማ የእያንዳንዱን ልጅ ጠንካራ ጎኖችና ድጋፍ "
                    "የሚፈልጉ ጎኖች ይለያል።"},
    ),
    (
        {"english": "Does New Life provide psychological support?",
         "amharic": "ኒው ላይፍ የስነ-ልቦና ድጋፍ ይሰጣል?"},
        {"english": "Yes. Psychological support is part of our approach to "
                    "child development.",
         "amharic": "አዎ። የስነ-ልቦና ድጋፍ የልጅ ልማት አቀራረባችን አንድ አካል ነው።"},
    ),
    (
        {"english": "Who can join the Parenting Academy?",
         "amharic": "የወላጅነት አካዳሚን ማን መቀላቀል ይችላል?"},
        {"english": "Anyone aged 18 or above who wants to learn parenting "
                    "skills. You do not need a child enrolled at New Life.",
         "amharic": "የወላጅነት ክህሎት ለመማር የሚፈልግ ከ18 ዓመት በላይ ማንኛውም ሰው። "
                    "ልጅዎ በኒው ላይፍ መመዝገቡ አስፈላጊ አይደለም።"},
    ),
    (
        {"english": "Do Parenting Academy participants get a certificate?",
         "amharic": "የወላጅነት አካዳሚ ተሳታፊዎች ሰርተፊኬት ያገኛሉ?"},
        {"english": "Yes, participants receive a certificate after completing "
                    "the program.",
         "amharic": "አዎ፣ ተሳታፊዎች ትምህርቱን ሲጨርሱ ሰርተፊኬት ያገኛሉ።"},
    ),
]


def faq_text(lang: str = "english") -> str:
    """Render the whole FAQ as one HTML message."""
    heading = "❓ <b>Frequently asked questions</b>" if lang == "english" else "❓ <b>ተደጋጋሚ ጥያቄዎች</b>"
    parts = [heading]
    for question, answer in FAQ:
        parts.append(f"\n<b>{pick(question, lang)}</b>\n{pick(answer, lang)}")
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
#  Fallback for anything not covered
# --------------------------------------------------------------------------- #
UNKNOWN_ANSWER = {
    "english": (
        "Thank you for your question! We want to make sure you receive "
        "accurate information, so a member of our team will help you with "
        "this.\n\n"
        "☎️ 0970535455\n"
        "✉️ Newlifetecenter@gmail.com\n\n"
        "🕗 Monday – Sunday, 8:00 AM – 6:00 PM"
    ),
    "amharic": (
        "ስለ ጥያቄዎ እናመሰግናለን! ትክክለኛ መረጃ ማግኘትዎን ለማረጋገጥ የቡድናችን አባል "
        "ይረዳዎታል።\n\n"
        "☎️ 0970535455\n"
        "✉️ Newlifetecenter@gmail.com\n\n"
        "🕗 ሰኞ – እሁድ፣ ከጠዋቱ 8:00 – ምሽቱ 6:00"
    ),
}
