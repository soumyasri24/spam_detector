"""Tiny JSON-file storage for reported and blocked phone numbers.

File layout (spam_numbers.json):
{
  "+15551234567": {"reported_at": "2026-10-16 10:30", "blocked": false}
}

"Blocked" here is only a flag saved in this file. It does NOT block
calls on your phone, carrier, or operating system.
"""

import json
import re
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "spam_numbers.json"


def validate_number(raw: str):
    """Check a phone number and return (clean_number, error_message).

    Accepts digits plus common separators: spaces, dashes, dots, parentheses,
    and an optional leading "+". Must contain 7 to 15 digits.
    """
    raw = raw.strip()
    if not raw:
        return None, "Please enter a phone number."
    if not re.fullmatch(r"\+?[\d\s\-().]+", raw):
        return None, "Use only digits, spaces, dashes, dots, parentheses, and an optional leading +."
    digits = re.sub(r"\D", "", raw)
    if not 7 <= len(digits) <= 15:
        return None, "A phone number should have between 7 and 15 digits."
    return ("+" if raw.startswith("+") else "") + digits, None


def load_numbers() -> dict:
    """Read the JSON file. Returns an empty dict if missing or unreadable."""
    if not DATA_FILE.exists():
        return {}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def report_number(number: str) -> bool:
    """Mark a number as spam. Returns False if it was already reported."""
    data = load_numbers()
    if number in data:
        return False
    data[number] = {
        "reported_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "blocked": False,
    }
    _save(data)
    return True


def block_number(number: str) -> bool:
    """Flag a reported number as blocked (local record only)."""
    data = load_numbers()
    if number not in data:
        return False
    data[number]["blocked"] = True
    _save(data)
    return True
