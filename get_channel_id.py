"""Helper: prints the numeric chat_id of your Telegram channel.

HOW TO USE
----------
1. Make sure the bot is admin of the channel with 'Post Messages' permission.
2. Post ANY text message in the channel (e.g. 'hello').
3. Within 24 hours, run this script:
       python get_channel_id.py
   (or trigger the GitHub workflow 'find-channel-id' — see README).
4. The script prints every chat Telegram has seen from your bot, including the channel's ID.
5. Copy the channel ID (a negative number like -1001234567890) into .env
   as TELEGRAM_CHAT_ID.

Notes:
- Telegram only shows channel_post updates for channels where the bot has admin rights.
- Updates are retained for 24 hours, so the channel post must be recent.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is not set in .env or environment")

API = f"https://api.telegram.org/bot{TOKEN}"


def main() -> int:
    try:
        r = requests.get(f"{API}/getUpdates", params={"timeout": 0}, timeout=30)
    except Exception as exc:
        print(f"Could not reach api.telegram.org: {exc}", file=sys.stderr)
        print("\nYour network may be blocking Telegram. Options:", file=sys.stderr)
        print("  1) Turn on a VPN and retry.", file=sys.stderr)
        print("  2) Run this via the 'find-channel-id' GitHub workflow instead.", file=sys.stderr)
        return 1

    data = r.json()
    if not data.get("ok"):
        print(f"Telegram API error: {data}", file=sys.stderr)
        return 1

    updates = data.get("result", [])
    if not updates:
        print("No updates found. Post a message in your channel first, then retry.")
        print("(Make sure the bot is admin of the channel with 'Post Messages' permission.)")
        return 0

    chats = {}
    for upd in updates:
        for key in ("channel_post", "message", "edited_channel_post", "edited_message"):
            if key in upd:
                c = upd[key]["chat"]
                chats[c["id"]] = (c.get("type"), c.get("title") or c.get("username") or "(no title)")

    print(f"Found {len(chats)} chat(s) the bot has received messages from:\n")
    for chat_id, (chat_type, title) in chats.items():
        marker = "  <-- use this" if chat_type == "channel" else ""
        print(f"  id={chat_id}  type={chat_type}  title={title!r}{marker}")

    channel_ids = [cid for cid, (ctype, _) in chats.items() if ctype == "channel"]
    if channel_ids:
        print(f"\n\u2713 Copy this into .env (or as the TELEGRAM_CHAT_ID GitHub secret):")
        print(f"  TELEGRAM_CHAT_ID={channel_ids[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
