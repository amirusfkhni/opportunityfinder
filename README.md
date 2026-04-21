# Opportunity Finder Bot

Scrapes research opportunities (symposia, workshops, summer schools, PhD/postdoc, internships) across Europe in drug discovery / structural bioinformatics / ML-for-drug-discovery and posts each one to your private Telegram channel.

## How it works

1. Every 3 hours, GitHub Actions runs `main.py`.
2. It pulls opportunities from all configured sources (RSS feeds + ELIXIR TeSS API).
3. It filters by keywords (see `config.py`) and keeps only items whose registration deadline hasn't passed.
4. A SQLite database (`data/opportunities.db`) remembers what was already sent, so you never get the same post twice.
5. New items are posted to your Telegram channel as formatted messages.

---

## One-time setup

### 1. Install Python dependencies (on your PC, for local testing)

Open PowerShell in this folder and run:

```powershell
python -m pip install -r requirements.txt
```

### 2. Get your channel's chat ID

The bot needs a **numeric** chat ID (like `-1001234567890`), not the `https://t.me/...` invite link.

1. Make sure your bot is an admin of the channel with "Post Messages" permission.
2. Post any message in the channel (e.g. `hello`).
3. Run the helper:
   ```powershell
   python get_channel_id.py
   ```
   (If your local network blocks Telegram's API, run the **find-channel-id** workflow on GitHub Actions instead.)
4. Copy the printed channel ID into `.env` as `TELEGRAM_CHAT_ID`.

### 3. Test it locally (optional — skip if Telegram API is blocked on your network)

```powershell
python main.py
```

### 4. Push to GitHub + enable scheduled runs

```powershell
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/amirusfkhni/opportunityfinder.git
git push -u origin main
```

Then on GitHub:

- Go to **Settings → Secrets and variables → Actions** and create:
  - `TELEGRAM_BOT_TOKEN` = your bot token
  - `TELEGRAM_CHAT_ID` = numeric chat ID (e.g. `-1001234567890`)
- Go to **Actions** tab, enable workflows, and click **Run workflow** on `opportunity-finder` once to test.

From this point the bot runs automatically every 3 hours, for free.

---

## Customizing

- **Add/remove keywords:** edit the `KEYWORDS` list in `config.py`.
- **Add more RSS feeds:** append entries to `RSS_FEEDS` in `config.py`.
- **Change schedule:** edit the `cron:` line in `.github/workflows/run.yml`.

## Files

| File | What it does |
|------|--------------|
| `main.py` | Orchestrator — run this to execute one cycle |
| `config.py` | Keywords + source list (edit this to tune) |
| `sources/rss.py` | Generic RSS/Atom puller |
| `sources/elixir_tess.py` | ELIXIR TeSS training events API |
| `filters.py` | Keyword relevance + deadline filter |
| `db.py` | SQLite dedup store |
| `telegram_poster.py` | Posts formatted messages to Telegram |
| `get_channel_id.py` | Helper to discover your channel's chat ID |
| `.github/workflows/run.yml` | GitHub Actions scheduler |
| `.github/workflows/find-channel-id.yml` | One-click workflow to find your channel ID |
