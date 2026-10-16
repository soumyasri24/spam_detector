"""Simple rule-based spam message detector.

Each rule looks for a pattern in the text and adds points to a score.
If the total score reaches SPAM_THRESHOLD, the message is labeled "Spam".

IMPORTANT: This module only reads the text. It never opens, visits,
or follows any link found in a message.
"""

import re

# Score needed to label a message as Spam. Lower = stricter.
SPAM_THRESHOLD = 3

# Each rule: (name, regex pattern, points, warning shown to the user)
RULES = [
    (
        "link",
        r"(https?://|www\.|\b[a-z0-9-]+\.(com|net|org|info|xyz|top|click|link|ly)\b)",
        2,
        "Contains a link. Do not click it, even if it looks familiar.",
    ),
    (
        "credentials",
        r"\b(password|passcode|otp|one[- ]time (code|password)|pin|cvv|login|verify your (account|identity)|ssn|social security)\b",
        3,
        "Asks for a password, code, or personal verification details.",
    ),
    (
        "payment",
        r"\b(payment|pay now|wire transfer|gift ?card|bitcoin|crypto|bank (account|details)|credit card|debit card|upi|send money|processing fee)\b",
        3,
        "Mentions payment or asks for money or card/bank details.",
    ),
    (
        "urgency",
        r"\b(urgent|immediately|act now|right away|final notice|last chance|expires? (today|soon|in)|within \d+ (hours?|minutes?)|account (suspended|locked|blocked)|limited time)\b",
        2,
        "Creates urgency to pressure you into acting quickly.",
    ),
    (
        "prize",
        r"\b(you('ve| have)? won|winner|congratulations|free (gift|prize|money)|claim your|lottery|jackpot)\b",
        2,
        "Promises a prize, reward, or free money.",
    ),
]


def check_message(text: str) -> dict:
    """Analyze a message and return a result dictionary.

    Returns:
        {
            "label": "Spam" or "Not Spam",
            "score": int,
            "reasons": list of warning strings,
        }
    """
    lowered = text.lower()
    score = 0
    reasons = []

    for _name, pattern, points, warning in RULES:
        if re.search(pattern, lowered):
            score += points
            reasons.append(warning)

    label = "Spam" if score >= SPAM_THRESHOLD else "Not Spam"
    return {"label": label, "score": score, "reasons": reasons}
