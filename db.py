"""SQLite dedup store. Tracks which opportunities have already been posted."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "opportunities.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,            -- hash of (source, url or title)
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT,
    deadline TEXT,
    posted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_source ON opportunities(source);
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(_SCHEMA)
    return conn


def already_posted(conn: sqlite3.Connection, opp_id: str) -> bool:
    cur = conn.execute("SELECT 1 FROM opportunities WHERE id = ?", (opp_id,))
    return cur.fetchone() is not None


def mark_posted(conn: sqlite3.Connection, opp_id: str, source: str, title: str,
                url: str | None, deadline: str | None, posted_at: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO opportunities (id, source, title, url, deadline, posted_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (opp_id, source, title, url, deadline, posted_at),
    )
    conn.commit()
