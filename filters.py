"""Relevance filtering via keyword matching + deadline sanity."""
from datetime import date, datetime
from config import KEYWORDS, MIN_KEYWORD_HITS


def is_relevant(text: str) -> bool:
    if not text:
        return False
    low = text.lower()
    hits = sum(1 for kw in KEYWORDS if kw.lower() in low)
    return hits >= MIN_KEYWORD_HITS


def is_still_open(deadline: datetime | date | None) -> bool:
    """Return True if no deadline is known, or deadline is today/future."""
    if deadline is None:
        return True
    if isinstance(deadline, datetime):
        return deadline.date() >= date.today()
    return deadline >= date.today()
