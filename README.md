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
2. Run the helper:
   ```powershell
   python get_channel_id.py
   ```
3. In Telegram, open the channel and post any message (e.g. `hello`).
4. The script will print your chat ID and tell you to paste it into `.env`.

Open `.env` in Notepad and fill in the line:
```
TELEGRAM_CHAT_ID=-1001234567890
```

### 3. Test it locally

```powershell
python main.py
```

You should see log lines like `Fetched 200 raw opportunities` → `30 relevant` → `30 new` → `Posted 30 opportunities`. Check your Telegram channel.

### 4. Push to GitHub + enable scheduled runs

1. Initialize git and push to the repo:
   ```powershell
   git init
   git add .
   git commit -m "initial commit"
   git branch -M main
   git remote add origin https://github.com/amirusfkhni/opportunityfinder.git
   git push -u origin main
   ```
   (The `.gitignore` prevents `.env` and your `.txt` secret files from being uploaded.)

2. Add your secrets on GitHub:
   - Go to https://github.com/amirusfkhni/opportunityfinder/settings/secrets/actions
   - Click **New repository secret** twice to create:
     - `TELEGRAM_BOT_TOKEN` = your bot token
     - `TELEGRAM_CHAT_ID` = your numeric chat ID (e.g. `-1001234567890`)

3. Enable Actions:
   - Go to the **Actions** tab of your repo.
   - If prompted, click **I understand my workflows, go ahead and enable them**.
   - You can manually trigger a run: Actions → `opportunity-finder` → **Run workflow**.

From this point the bot runs automatically every 3 hours, forever, for free.

---

## Customizing

- **Add/remove keywords:** edit the `KEYWORDS` list in `config.py`.
- **Add more RSS feeds:** append entries to `RSS_FEEDS` in `config.py`.
- **Change schedule:** edit the `cron:` line in `.github/workflows/run.yml`. Examples:
  - Every hour: `0 * * * *`
  - Every 6 hours: `0 */6 * * *`
  - Once a day at 08:00 UTC: `0 8 * * *`

---

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

---

## Future improvements (optional)

- Add more sources: EMBL events, Max Planck calendar, per-institution career pages
- Gmail-ingest module: forward LinkedIn job alerts to Gmail → bot reads via IMAP
- LLM-based relevance scoring (for when keyword matching gets noisy)
- Daily digest mode (one summary post per day instead of one post per opportunity)
