"""Posts formatted opportunities to a Telegram channel via Bot API."""
import html
import os
import time
import requests
from config import HTTP_TIMEOUT, POST_DELAY_SECONDS

API = "https://api.telegram.org/bot{token}/{method}"


def _escape(s: str | None) -> str:
    return html.escape(s or "", quote=False)


def format_message(opp) -> str:
    """Build an HTML-formatted Telegram message from an Opportunity."""
    parts = [f"<b>{_escape(opp.title)}</b>"]
    if opp.description:
        desc = opp.description.strip()
        if len(desc) > 700:
            desc = desc[:700].rsplit(" ", 1)[0] + "…"
        parts.append("")
        parts.append(_escape(desc))

    meta = []
    if opp.start_date or opp.end_date:
        when = f"{opp.start_date or '?'}"
        if opp.end_date and opp.end_date != opp.start_date:
            when += f" → {opp.end_date}"
        meta.append(f"<b>When:</b> {_escape(when)}")
    if opp.deadline:
        meta.append(f"<b>Deadline:</b> {_escape(str(opp.deadline))}")
    if opp.location:
        meta.append(f"<b>Location:</b> {_escape(opp.location)}")
    meta.append(f"<b>Source:</b> {_escape(opp.source)}")
    if opp.url:
        meta.append(f'<b>Link:</b> <a href="{_escape(opp.url)}">Open page</a>')

    if meta:
        parts.append("")
        parts.extend(meta)

    return "\n".join(parts)


def send_message(token: str, chat_id: str, text: str) -> dict:
    r = requests.post(
        API.format(token=token, method="sendMessage"),
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=HTTP_TIMEOUT,
    )
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data


def post_opportunity(opp) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    send_message(token, chat_id, format_message(opp))
    time.sleep(POST_DELAY_SECONDS)
