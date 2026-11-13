"""Application-wide constants shared across the system."""

from __future__ import annotations

from enum import Enum


class RegistrationStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    CLASS_ASSIGNED = "class_assigned"
    ENROLLED = "enrolled"
    REJECTED = "rejected"


class ScheduleAvailability(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    FULL = "full"


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"


class NotificationType(str, Enum):
    REGISTRATION_SUBMITTED = "registration_submitted"
    REGISTRATION_APPROVED = "registration_approved"
    REGISTRATION_REJECTED = "registration_rejected"
    CLASS_ASSIGNED = "class_assigned"
    REGISTRATION_COMPLETED = "registration_completed"
    DUPLICATE_ALERT = "duplicate_alert"
    REMINDER_INCOMPLETE = "reminder_incomplete"
    REMINDER_CLASS = "reminder_class"
    REMINDER_PAYMENT = "reminder_payment"
    MANUAL_REPLY = "manual_reply"
    SYSTEM = "system"


class DocumentType(str, Enum):
    STUDENT_PHOTO = "student_photo"
    PARENT_ID = "parent_id"
    BIRTH_CERTIFICATE = "birth_certificate"
    PAYMENT_RECEIPT = "payment_receipt"
    OTHER = "other"


# Development demo content for New Life Training Center.
# Replace with official information before production.
DEMO_PROGRAMS = {
    "kids": {
        "name": "Kids Program",
        "name_am": "�Wizard Kids ቭግ",
        "description": (
            "The Kids Program focuses on building confidence, "
            "social skills, and emotional intelligence through "
            "structured activities, group games, and guided "
            "developmental exercises."
        ),
        "description_am": (
            "ትምህርት ሰራተኞች መልህቅ ፊተኞችንን, ቀይቋቸውን እና "
            "አደረጃ እንቅስቃሴዎችን በመቀናሰ ትምህርት ላይ ይዟል።"
        ),
        "objectives": [
            "Confidence and self-esteem",
            "Communication skills",
            "Leadership",
            "Emotional intelligence",
            "Social skills",
            "Critical thinking and problem-solving",
            "Academic performance",
            "Time management",
            "Public speaking",
            "Independence and responsibility",
        ],
        "eligibility": "Ages 4-12",
        "duration": "8 weeks (per session)",
        "location": "[Configurable]",
        "tuition_fee": "[Configurable]",
        "schedules": [],
        "benefits": "Safe, structured environment for early development.",
        "sponsorship": "Scholarships available on request.",
        "registration_available": True,
    },
    "parenting": {
        "name": "Parenting Course",
        "name_am": "የእግዚአብሔር ትምህርት ማስረጃ ተጽዕኖች",
        "description": "A course helping parents build effective parenting skills and family communication.",
        "description_am": "የእግዚአብሔር ትምህርት ማስረጃ ተጽዕኖች የሚያበክሉ ተባይዎችን እና ክፍလ አቀጣጫ ማግኘት ትምህርት ይርዝር ይረዳል።",
        "objectives": [
            "Positive parenting techniques",
            "Family communication",
            "Child development knowledge",
            "Stress management",
            "Setting boundaries",
        ],
        "eligibility": "Open to all parents and guardians",
        "duration": "6 weeks",
        "location": "[Configurable]",
        "tuition_fee": "[Configurable]",
        "schedules": [],
        "benefits": "Practical tools for everyday parenting challenges.",
        "sponsorship": "Financial aid available for qualifying families.",
        "registration_available": True,
    },
}

# Default demo notifications recipients (staff chat IDs).
DEMO_NOTIFICATION_RECIPIENTS = [123456789]

# Status labels for user-facing display.
STATUS_LABELS = {
    RegistrationStatus.PENDING_REVIEW: ("Pending Review", "ደረጃ ዝበቂኝ"),
    RegistrationStatus.APPROVED: ("Approved", "ተመረጠ"),
    RegistrationStatus.CLASS_ASSIGNED: ("Class Assigned", "መገባት ተመረጠ"),
    RegistrationStatus.ENROLLED: ("Enrolled", "ተቀናሰ"),
    RegistrationStatus.REJECTED: ("Rejected", "አብ promotions"),
}
