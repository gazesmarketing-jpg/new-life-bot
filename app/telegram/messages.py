"""Bilingual (Amharic/English) Telegram message templates.

All user-facing bot text lives here so translators and New Life staff can
edit copy without touching handler code.
"""

from __future__ import annotations


def t(key: str, lang: str = "english") -> str:
    """Return the message for *key* in the requested language.

    Keys follow the pattern: section:topic:key
    Supported languages: 'english', 'amharic'
    """
    # Simple dictionary; extensible via YAML/JSON later.
    data = {
        "menu:main": {
            "english": "◈  Main Menu",
            "amharic": "◈  መሳሪያ አስፈጀ",
        },
        "menu:register_child": {
            "english": "Register a Child",
            "amharic": "ወለቱ ጤ ሰኔ",
        },
        "menu:parenting_course": {
            "english": "Register for Parenting Course",
            "amharic": "የፊተኞች ትምህርት መረዳት መረዳት",
        },
        "menu:explore_programs": {
            "english": "Explore Programs",
            "amharic": "ትምህርት ማያወቅ",
        },
        "menu:info": {
            "english": "Training Center Information",
            "amharic": "ትምህርት መድሳት ዝርዝር",
        },
        "menu:my_registrations": {
            "english": "My Registrations",
            "amharic": "የእኔ መረዳቶች",
        },
        "menu:contact": {
            "english": "Contact New Life",
            "amharic": "ኔዊ ሊፈ ነገር",
        },
        "menu:change_language": {
            "english": "Change Language",
            "amharic": "ቋንቋን ፍቀሬ ስተመ",
        },
        "start": {
            "english": "Welcome to New Life Training Center!",
            "amharic": "ኔዊ ሊፈ ትምህርት መድሳት ጋር ይዞል!",
        },
        "welcome_intro": {
            "english": "We are happy to help you register your child or enroll in our parenting course. Select an option below.",
            "amharic": "ሁለቱም ለማወቅ ጤሰኞችን እና ተባይዎችን በትምህርት ውስጥ ተጽዕኖችን ለማወቅ ይጠቁም።",
        },
        "lang_select": {
            "english": "Please select your language:",
            "amharic": "ቋንቋዎን አምራቱ።",
        },
        "lang_english": {
            "english": "English",
            "amharic": "English",
        },
        "lang_amharic": {
            "english": "አማርኛ",
            "amharic": "አማርኛ",
        },
        "child_registration:info": {
            "english": "Let's register your child for the Kids Program. We will collect the required details step by step.",
            "amharic": "ጤዎንን Kids Program መረዳት ለማወቅ አገልግሎት ይለያዩ። የተለያዩ ዝርዝሮችን በመጠቀም ይለያዩ።",
        },
        "child_registration:name": {
            "english": "Child's full name",
            "amharic": "ጤዎን ስም ስም",
        },
        "child_registration:name_hints": {
            "english": "Full name as it appears on school records",
            "amharic": "በመዝገብ ቤት ውስጥ የሚያስተዳድረው ውስጥ",
        },
        "child_registration:dob_or_age": {
            "english": "Date of birth or age",
            "amharic": "የትወንት ወይም ዕድሜ",
        },
        "child_registration:gender": {
            "english": "Gender",
            "amharic": "እምነት",
        },
        "child_registration:school": {
            "english": "School name",
            "amharic": "መዝገብ ቤት",
        },
        "child_registration:grade": {
            "english": "Grade / Class",
            "amharic": "መልሲ / ተቋም",
        },
        "child_registration:parent_name": {
            "english": "Parent / guardian full name",
            "amharic": "የእግዚአብሔር ስም ስም ወይም ጤዎን ስም ስም",
        },
        "child_registration:phone": {
            "english": "Parent / guardian phone number",
            "amharic": "የእግዚአብሔር ስም ስም ወይም ስም",
        },
        "child_registration:address": {
            "english": "Home address or sub-city",
            "amharic": "የእግዚአብሔር ስም ስም ወይም ስም",
        },
        "child_registration:previous_training": {
            "english": "Previous training experience",
            "amharic": "የፊተኞች መዝገብ ቤት",
        },
        "child_registration:goals": {
            "english": "Select development goals (you may choose multiple):",
            "amharic": "የትምህርት ማያወቅ",
        },
        "goals:confidence": {
            "english": "Confidence and self-esteem",
            "amharic": "ፊተኞችን",
        },
        "goals:communication": {
            "english": "Communication skills",
            "amharic": "ተጽዕኖችን",
        },
        "goals:leadership": {
            "english": "Leadership",
            "amharic": "ወዳጅ",
        },
        "goals:emotional_intelligence": {
            "english": "Emotional intelligence",
            "amharic": "ማስታወሻን",
        },
        "goals:social_skills": {
            "english": "Social skills",
            "amharic": "ስነ-ሰብ",
        },
        "goals:critical_thinking": {
            "english": "Critical thinking and problem-solving",
            "amharic": "የሰውና ማስተካከያ",
        },
        "goals:academic": {
            "english": "Academic performance",
            "amharic": "ተልባ ማጠናቀቅ",
        },
        "goals:time_management": {
            "english": "Time management",
            "amharic": "የመዝገብ ቤት",
        },
        "goals:speaking": {
            "english": "Public speaking",
            "amharic": "የመዝገብ ቤት",
        },
        "goals:responsibility": {
            "english": "Independence and responsibility",
            "amharic": "የመዝገብ ቤት",
        },
        "parenting_course:info": {
            "english": "Let's register for the Parenting Course.",
            "amharic": "የእግዚአብሔር ትምህርት መዝገብ",
        },
        "parenting_course:name": {
            "english": "Full name",
            "amharic": "ስም",
        },
        "parenting_course:phone": {
            "english": "Phone number",
            "amharic": "ቁጥር",
        },
        "parenting_course:address": {
            "english": "Address",
            "amharic": "የእግዚአብሔር ስም ስም",
        },
        "parenting_course:schedule": {
            "english": "Preferred schedule (if applicable)",
            "amharic": "የተለያዩ ትምህርት",
        },
        "parenting_course:submit": {
            "english": "Submit registration",
            "amharic": "መረዳት መቀየር",
        },
        "child_registration:validation:missing": {
            "english": "This field is required.",
            "amharic": "ይህ ዝርዝር አለ።",
        },
        "child_registration:validation:phone": {
            "english": "Please enter a valid phone number.",
            "amharic": "እባክዎን ቁጥር አለ።",
        },
        "confirmation:summary": {
            "english": "Registration Summary",
            "amharic": "መረዳት መልሰር",
        },
        "confirmation:submit": {
            "english": "Submit Registration",
            "amharic": "መረዳት መቀየር",
        },
        "confirmation:number": {
            "english": "Registration number: ",
            "amharic": "መረዳት ቁጥር: ",
        },
        "confirmation:status": {
            "english": "Status: Pending Review",
            "amharic": "ሰቀረ ፍቀሬ",
        },
        "confirmation:next_steps": {
            "english": "You will receive updates by this chat. Staff will review your registration.",
            "amharic": "ሁለቱም በትምህርት ውስጥ ይሰጣሉም። ስታፍት እርምጃዎችን ይጠቁም።",
        },
        "error": {
            "english": "An error occurred. Please try again.",
            "amharic": "ግንኙነት ይለያዩ።",
        },
        "error:wrong_lang": {
            "english": "Please select your language first.",
            "amharic": "ቋንቋዎን አምራቱ።",
        },
        "status:pending": {
            "english": "Pending Review",
            "amharic": "ደረጃ ዝበቂኝ",
        },
        "status:approved": {
            "english": "Approved",
            "amharic": "ተመረጠ",
        },
        "status:class_assigned": {
            "english": "Class Assigned",
            "amharic": "መገባት ተመረጠ",
        },
        "status:enrolled": {
            "english": "Enrolled",
            "amharic": "ተቀናሰ",
        },
        "status:rejected": {
            "english": "Rejected",
            "amharic": "አብ promotions",
        },
        "contact:info": {
            "english": "Contact New Life Training Center",
            "amharic": "ኔዊ ሊፈ ትምህርት መድሳት",
        },
        "contact:info_text": {
            "english": "Phone: [Configurable] | Email: [Configurable] | Office hours: [Configurable]",
            "amharic": "የእግዚአብሔር መዝገብ",
        },
        "programs:kids": {
            "english": "Kids Program",
            "amharic": "Kvids Program",
        },
        "programs:parenting": {
            "english": "Parenting Course",
            "amharic": "የእግዚአብሔር ትምህርት",
        },
        "programs:sections": {
            "english": "Select a section to view details:",
            "amharic": "የተለያዩ አንድ",
        },
    }
    try:
        return data.get(key, {}).get(lang, data.get(key, {}).get("english", key))
    except Exception:
        return key
