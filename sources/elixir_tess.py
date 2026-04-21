"""ELIXIR TeSS — bioinformatics training events across Europe.

Uses the public JSON:API at https://tess.elixir-europe.org
Docs: https://tess.elixir-europe.org/api
"""
from __future__ import annotations
import logging
from datetime import date
from typing import Iterator

import requests
from dateutil import parser as dateparser

from config import HTTP_TIMEOUT, TESS_API_URL, TESS_ENABLED, TESS_PAGES, USER_AGENT
from .base import Opportunity

log = logging.getLogger(__name__)


def _parse_date(val: str | None) -> date | None:
    if not val:
        return None
    try:
        return dateparser.parse(val).date()
    except (ValueError, TypeError):
        return None


def fetch_all() -> Iterator[Opportunity]:
    if not TESS_ENABLED:
        return

    headers = {"Accept": "application/vnd.api+json", "User-Agent": USER_AGENT}

    for page in range(1, TESS_PAGES + 1):
        params = {"page[number]": page, "page[size]": 20, "sort": "-created-at"}
        try:
            r = requests.get(TESS_API_URL, params=params, headers=headers, timeout=HTTP_TIMEOUT)
            r.raise_for_status()
        except Exception as exc:
            log.warning("TeSS fetch failed page=%s: %s", page, exc)
            return

        payload = r.json()
        data = payload.get("data", [])
        if not data:
            return

        for item in data:
            attrs = item.get("attributes", {}) or {}
            title = attrs.get("title") or "(untitled)"
            desc = attrs.get("description") or ""
            url = attrs.get("url") or attrs.get("external-url")
            start = _parse_date(attrs.get("start"))
            end = _parse_date(attrs.get("end"))

            location = None
            city = attrs.get("city")
            country = attrs.get("country")
            venue = attrs.get("venue")
            loc_bits = [b for b in (venue, city, country) if b]
            if loc_bits:
                location = ", ".join(loc_bits)

            yield Opportunity(
                source="ELIXIR TeSS",
                title=title,
                description=desc,
                url=url,
                start_date=start,
                end_date=end,
                location=location,
            )
