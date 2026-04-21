"""Configuration: keywords to match and sources to fetch."""

# Any opportunity matching at least one keyword (case-insensitive, substring match)
# is considered relevant. Expand freely.
KEYWORDS = [
    # Core drug discovery
    "drug discovery", "drug design", "drug development",
    "medicinal chemistry", "pharmaceutical",
    "lead optimization", "lead identification", "hit-to-lead",
    "drug repurposing", "drug repositioning",

    # Computational / structure-based
    "virtual screening", "molecular docking", "docking",
    "structure-based", "structure based",
    "structural bioinformatics", "structural biology",
    "cheminformatics", "chemoinformatics",
    "CADD", "computer-aided drug", "computer aided drug",
    "pharmacophore", "QSAR", "ADMET",
    "molecular dynamics", "free energy",
    "protein-ligand", "protein ligand",
    "fragment-based", "fragment based",
    "computational chemistry", "computational biology",

    # ML / AI for drug discovery
    "machine learning drug", "deep learning drug", "AI drug",
    "ML drug discovery", "AI-driven drug", "generative chemistry",
    "generative model drug", "artificial intelligence drug",

    # Therapeutic focus
    "antibacterial", "antibiotic", "antimicrobial",
    "antiviral", "antifungal", "AMR", "antimicrobial resistance",

    # Related
    "cryo-EM drug", "protein structure prediction",
    "alphafold drug", "binding affinity",
]

# Minimum fraction of keyword hits — simple threshold. Any single hit is enough.
MIN_KEYWORD_HITS = 1

# RSS / Atom feeds. Each entry will be fetched via feedparser.
# Many sources let you build a search RSS URL with your own keywords — do that where possible.
# If a feed URL stops working, just remove or replace it here.
RSS_FEEDS = [
    # arXiv q-bio biomolecules (papers + occasional CFPs; mostly used to catch workshop announcements)
    {"name": "arXiv q-bio.BM", "url": "http://export.arxiv.org/rss/q-bio.BM"},
    {"name": "arXiv q-bio.QM", "url": "http://export.arxiv.org/rss/q-bio.QM"},

    # WikiCFP — call-for-papers aggregator, has RSS per category
    {"name": "WikiCFP bioinformatics", "url": "http://www.wikicfp.com/cfp/rss?cat=bioinformatics"},
    {"name": "WikiCFP drug discovery", "url": "http://www.wikicfp.com/cfp/rss?cat=drug+discovery"},
    {"name": "WikiCFP machine learning", "url": "http://www.wikicfp.com/cfp/rss?cat=machine+learning"},

    # EURAXESS search RSS — EU-wide research jobs/PhD/postdoc.
    # You can generate your own by going to https://euraxess.ec.europa.eu/jobs/search, filtering,
    # and clicking the RSS icon. Feel free to add more below.
    {"name": "EURAXESS: drug discovery", "url": "https://euraxess.ec.europa.eu/jobs/search/rss?keywords=drug+discovery"},
    {"name": "EURAXESS: bioinformatics", "url": "https://euraxess.ec.europa.eu/jobs/search/rss?keywords=bioinformatics"},
    {"name": "EURAXESS: computational biology", "url": "https://euraxess.ec.europa.eu/jobs/search/rss?keywords=computational+biology"},

    # Nature Careers — job/internship feeds by keyword
    {"name": "Nature Careers: drug discovery", "url": "https://www.nature.com/naturecareers/jobs/rss?query=drug+discovery"},
    {"name": "Nature Careers: bioinformatics", "url": "https://www.nature.com/naturecareers/jobs/rss?query=bioinformatics"},

    # FindAPhD — UK+EU PhDs
    {"name": "FindAPhD: drug discovery", "url": "https://www.findaphd.com/phds/rss.aspx?Keywords=drug+discovery"},
    {"name": "FindAPhD: bioinformatics", "url": "https://www.findaphd.com/phds/rss.aspx?Keywords=bioinformatics"},
]

# ELIXIR TeSS — bioinformatics training events & courses across Europe.
# Public JSON:API, no key needed. Perfect for workshops/summer schools in your field.
TESS_ENABLED = True
TESS_API_URL = "https://tess.elixir-europe.org/events.json_api"
TESS_PAGES = 5   # 20 events per page; 5 = last ~100 events fetched per run

# Limits
MAX_POSTS_PER_RUN = 50         # safety cap; prevents channel spam on first run
POST_DELAY_SECONDS = 3          # delay between Telegram posts (rate limit safety)
HTTP_TIMEOUT = 25
USER_AGENT = "OpportunityFinderBot/1.0 (+https://github.com/amirusfkhni/opportunityfinder)"
