# Telegram Bot - Configuration

This bot is designed to be a full-featured Telegram bot rebuilt from scratch.

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# Bot token from @BotFather
BOT_TOKEN=your_telegram_bot_token_here

# Owner (admin) user id - commands restricted to this user
OWNER_USER_ID=123456789

# Database URL (SQLite by default)
DATABASE_URL=sqlite:///./bot.db

# Logging level
LOG_LEVEL=INFO

# Scheduler interval (seconds) - for recurring tasks
SCHEDULER_INTERVAL=300
```

## Project Structure

```
telegram_bot/
├── config.py           # Configuration management
├── database.py         # Database engine and session
├── bot.py              # Bot entry point
├── handlers/           # Command and callback handlers
│   ├── __init__.py
│   ├── commands.py     # /start, /help, /status, etc.
│   ├── inline.py       # Inline keyboard and callback handlers
│   └── states.py       # Conversation state machine
├── models/             # Database models
│   ├── __init__.py
│   └── user.py         # User state model
├── services/           # Business logic
│   ├── __init__.py
│   └── scheduler.py    # Recurring jobs scheduler
├── utils/              # Utility functions
│   ├── __init__.py
│   └── logging.py      # Logging setup
└── tests/              # Unit tests
    └── test_*.py
```

## Running the Bot

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python -m telegram_bot.bot
```

## Additional Notes

- The bot uses aiogram v3.x
- Database uses SQLAlchemy with SQLite
- Supports conversation states and inline keyboards
- Includes a scheduler for recurring tasks
- Logging configured with rotation
