# Project Structure for New Life Training Center System

## Top-level layout
    new-life/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                  # FastAPI application entry point
    │   ├── config.py                # Application settings (Pydantic Settings)
    │   ├── database.py              # SQLAlchemy engine, session, Base
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── security.py          # Password hashing, JWT tokens
    │   │   ├── permissions.py       # Role/permission definitions
    │   │   └── constants.py         # Shared constants (statuses, roles)
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py              # User (staff) model
    │   │   ├── parent.py            # Parent/guardian model
    │   │   ├── student.py           # Student/child model
    │   │   ├── registration.py      # Registration model
    │   │   ├── program.py           # Program model
    │   │   ├── class_schedule.py    # Class + schedule models
    │   │   ├── document.py          # Document model
    │   │   ├── payment.py           # Payment record model
    │   │   ├── schedule_assignments.py  # Class assignment model
    │   │   ├── notification.py      # Notification model
    │   │   └── audit_log.py         # Audit log model
    │   ├── schemas/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── parent.py
    │   │   ├── student.py
    │   │   ├── registration.py
    │   │   ├── program.py
    │   │   ├── class_schedule.py
    │   │   ├── document.py
    │   │   ├── payment.py
    │   │   ├── schedule_assignment.py
    │   │   ├── notification.py
    │   │   └── audit_log.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── deps.py              # FastAPI dependencies (auth, roles)
    │   │   ├── health.py            # Health check endpoint
    │   │   ├── users.py             # Staff user CRUD endpoints
    │   │   ├── registrations.py     # Registration CRUD endpoints
    │   │   ├── students.py          # Student management endpoints
    │   │   ├── programs.py          # Program management endpoints
    │   │   ├── classes.py           # Class/schedule management endpoints
    │   │   ├── documents.py         # Document upload/management endpoints
    │   │   ├── payments.py          # Payment record endpoints
    │   │   ├── reports.py           # Reports and CSV export endpoints
    │   │   └── notifications.py     # Notification endpoints
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── registration_service.py  # Core registration business logic
    │   │   ├── notification_service.py  # Notification dispatch and templates
    │   │   ├── reminder_service.py      # Reminder scheduling and dispatch
    │   │   ├── document_service.py      # Document upload, validation, storage
    │   │   ├── notion_service.py        # NotionSync interface (stub + docs)
    │   │   ├── export_service.py        # CSV export generation
    │   │   └── audit_service.py         # Audit log recording
    │   ├── telegram/
    │   │   ├── __init__.py
    │   │   ├── bot.py               # Telegram bot entry point
    │   │   ├── dispatcher.py        # Handler dispatcher setup
    │   │   ├── handlers/
    │   │   │   ├── __init__.py
    │   │   │   ├── setup.py
    │   │   │   ├── main_menu.py
    │   │   │   ├── child_registration.py
    │   │   │   ├── parenting_course.py
    │   │   │   ├── account.py
    │   │   │   └── notifications.py
    │   │   ├── knowledge.py         # Official center, program, fee and FAQ facts
    │   │   ├── messages.py          # Bilingual (Amharic/English) message templates
    │   │   └── utils.py             # Keyboard builders, state helpers
    │   ├── templates/
    │   │   ├── base.html
    │   │   ├── login.html
    │   │   ├── dashboard.html
    │   │   ├── registrations.html
    │   │   ├── registration_detail.html
    │   │   ├── students.html
    │   │   ├── students_detail.html
    │   │   ├── programs.html
    │   │   ├── classes.html
    │   │   ├── documents.html
    │   │   ├── finance.html
    │   │   ├── reports.html
    │   │   ├── staff.html
    │   │   └── errors.html
    │   ├── static/
    │   │   ├── css/
    │   │   │   └── style.css
    │   │   └── js/
    │   │       └── app.js
    │   └── uploads/                    # Persistent document storage (via Docker volume)
    ├── migrations/
    │   └── versions/
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py               # Test fixtures (test DB, test client)
    │   ├── test_auth.py
    │   ├── test_registrations.py
    │   ├── test_classes.py
    │   ├── test_notifications.py
    │   └── test_reports.py
    ├── .env.example                   # Environment variable template
    ├── Dockerfile                     # Production container
    ├── docker-compose.yml             # Dev + prod orchestration
    ├── alembic.ini
    ├── pyproject.toml
    ├── README.md
    ├── setup_guide.md
    ├── backup_restore_guide.md
    ├── admin_user_guide.md
    └── known_limitations.md
