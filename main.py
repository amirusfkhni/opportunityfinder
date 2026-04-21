"""Orchestrator: fetch all sources, filter, dedupe, post to Telegram."""
from __future__ import annotations
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from config import MAX_POSTS_PER_RUN  # noqa: E402
from db import already_posted, connect, mark_posted  # noqa: E402
from filters import is_relevant, is_still_open  # noqa: E402
from sources import elixir_tess, rss  # noqa: E402
from sources.base import Opportunity  # noqa: E402
from telegram_poster import post_opportunity  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("bot")


def collect_all() -> list[Opportunity]:
    opps: list[Opportunity] = []
    log.info("Fetching RSS feeds…")
    opps.extend(list(rss.fetch_all()))
    log.info("Fetching ELIXIR TeSS…")
    opps.extend(list(elixir_tess.fetch_all()))
    log.info("Fetched %d raw opportunities", len(opps))
    return opps


def _sort_key(o: Opportunity):
    # Soonest deadline first; fall back to start date; then unknowns last
    return (
        o.deadline or o.start_date or datetime(9999, 1, 1).date(),
    )


def main() -> int:
    if not os.environ.get("TELEGRAM_BOT_TOKEN"):
        log.error("TELEGRAM_BOT_TOKEN not set")
        return 2
    if not os.environ.get("TELEGRAM_CHAT_ID"):
        log.error("TELEGRAM_CHAT_ID not set — run get_channel_id.py first")
        return 2

    opps = collect_all()

    # Filter: relevance + still-open deadline
    relevant = [o for o in opps if is_relevant(o.searchable_text()) and is_still_open(o.deadline)]
    log.info("%d relevant & still-open", len(relevant))

    # Dedup against DB
    conn = connect()
    new_opps = [o for o in relevant if not already_posted(conn, o.stable_id())]
    log.info("%d new (not previously posted)", len(new_opps))

    new_opps.sort(key=_sort_key)
    to_post = new_opps[:MAX_POSTS_PER_RUN]

    posted = 0
    now = datetime.utcnow().isoformat()
    for opp in to_post:
        try:
            post_opportunity(opp)
            mark_posted(
                conn, opp.stable_id(), opp.source, opp.title, opp.url,
                str(opp.deadline) if opp.deadline else None, now,
            )
            posted += 1
        except Exception as exc:
            log.exception("Failed posting %r: %s", opp.title, exc)

    log.info("Posted %d opportunities", posted)
    if len(new_opps) > MAX_POSTS_PER_RUN:
        log.info("%d more will be posted on next run", len(new_opps) - MAX_POSTS_PER_RUN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
