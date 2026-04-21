"""Generic RSS/Atom puller — configurable list of feeds."""
from __future__ import annotations
import logging
from datetime import date
from typing import Iterator

import feedparser
from dateutil import parser as dateparser

from config import RSS_FEEDS, USER_AGENT
from .base import Opportunity

log = logging.getLogger(__name__)


def _parse_date(val: str | None) -> date | None:
    if not val:
        return None
    try:
        return dateparser.parse(val, fuzzy=True).date()
    except (ValueError, TypeError, OverflowError):
        return None


def fetch_all() -> Iterator[Opportunity]:
    for feed in RSS_FEEDS:
        name, url = feed["name"], feed["url"]
        try:
            parsed = feedparser.parse(url, agent=USER_AGENT)
        except Exception as exc:
            log.warning("RSS fetch failed: %s (%s): %s", name, url, exc)
            continue

        if parsed.bozo and not parsed.entries:
            log.warning("RSS parse error: %s (%s): %s", name, url, parsed.bozo_exception)
            continue

        for entry in parsed.entries:
            title = entry.get("title") or "(untitled)"
            desc = entry.get("summary") or entry.get("description") or ""
            link = entry.get("link")
            pub = _parse_date(entry.get("published") or entry.get("updated"))

            yield Opportunity(
                source=name,
                title=title,
                description=desc,
                url=link,
                start_date=pub,
            )
