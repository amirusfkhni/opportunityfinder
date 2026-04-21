"""Normalized opportunity record + hashing helper."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from hashlib import sha1


@dataclass
class Opportunity:
    source: str
    title: str
    description: str = ""
    url: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    deadline: date | None = None
    location: str | None = None
    extra: dict = field(default_factory=dict)

    def stable_id(self) -> str:
        key = f"{self.source}|{self.url or self.title}".encode("utf-8")
        return sha1(key).hexdigest()

    def searchable_text(self) -> str:
        bits = [self.title, self.description, self.location or ""]
        return " ".join(b for b in bits if b)
