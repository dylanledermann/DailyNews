# lean and confidence taken from www.allsides.com
# Initial values generated from Claude. Current values are in sources.json and taken directly from the website

SOURCES = [

    # -------------------------
    # U.S. GENERAL NEWS
    # -------------------------
    {
        # Associated Press dropped RSS - use Google News source filter instead
        "name": "Associated Press",
        "lean": "Center",
        "credibility": "High",
        "feed_type": "google_news",
        "feeds": [
            "https://news.google.com/rss/search?q=site%3Aapnews.com&hl=en-US&gl=US&ceid=US%3Aen"
        ]
    },
    {
        # Reuters dropped native RSS in 2020 — use Google News source filter instead
        "name": "Reuters",
        "lean": "Center",
        "credibility": "High",
        "feed_type": "google_news",
        "feeds": [
            "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen"
        ],
        "note": "Google News proxy — resolve redirect URLs before scraping"
    },
    {
        "name": "NPR",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://feeds.npr.org/1001/rss.xml",       # News
            "https://feeds.npr.org/1014/rss.xml",       # Politics
            "https://feeds.npr.org/1019/rss.xml",       # Technology
            "https://feeds.npr.org/1128/rss.xml",       # Health
            "https://feeds.npr.org/1007/rss.xml",       # Science
        ]
    },
    {
        "name": "The Hill",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://thehill.com/rss/syndicator/19110",  # Top Stories
        ]
    },
    {
        "name": "Axios",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://api.axios.com/feed/",
        ]
    },
    {
        "name": "New York Times News",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/Health.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        ]
    },
    {
        "name": "Washington Post",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://feeds.washingtonpost.com/rss/world",
            "https://feeds.washingtonpost.com/rss/national",
            "https://feeds.washingtonpost.com/rss/politics",
            "https://feeds.washingtonpost.com/rss/business",
            "https://feeds.washingtonpost.com/rss/technology",
            "https://feeds.washingtonpost.com/rss/lifestyle",
        ]
    },
    {
        "name": "Wall Street Journal",
        "lean": "Center-Right",
        "credibility": "High",
        "feeds": [
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
            "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
            "https://feeds.a.dj.com/rss/RSSWSJD.xml",          # Tech
            "https://feeds.a.dj.com/rss/RSSOpinion.xml",
        ]
    },
    {
        "name": "Fox News",
        "lean": "Right",
        "credibility": "Mixed",
        "feeds": [
            "https://moxie.foxnews.com/google-publisher/latest.xml",
            "https://moxie.foxnews.com/google-publisher/politics.xml",
            "https://moxie.foxnews.com/google-publisher/us.xml",
            "https://moxie.foxnews.com/google-publisher/world.xml",
            "https://moxie.foxnews.com/google-publisher/health.xml",
            "https://moxie.foxnews.com/google-publisher/tech.xml",
        ]
    },
    {
        "name": "The Guardian",
        "lean": "Left",
        "credibility": "High",
        "feeds": [
            "https://www.theguardian.com/world/rss",
            "https://www.theguardian.com/us-news/rss",
            "https://www.theguardian.com/politics/rss",
            "https://www.theguardian.com/technology/rss",
            "https://www.theguardian.com/science/rss",
            "https://www.theguardian.com/business/rss",
            "https://www.theguardian.com/environment/rss",
        ]
    },
    {
        "name": "The Atlantic",
        "lean": "Left",
        "credibility": "High",
        "feeds": [
            "https://news.google.com/rss/search?q=site%3Atheatlantic.com&hl=en-US&gl=US&ceid=US%3Aen",
        ]
    },

    # -------------------------
    # INTERNATIONAL
    # -------------------------
    {
        "name": "BBC News",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://feeds.bbci.co.uk/news/rss.xml",            # Top stories
            "https://feeds.bbci.co.uk/news/world/rss.xml",
            "https://feeds.bbci.co.uk/news/uk/rss.xml",
            "https://feeds.bbci.co.uk/news/technology/rss.xml",
            "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
            "https://feeds.bbci.co.uk/news/health/rss.xml",
            "https://feeds.bbci.co.uk/news/business/rss.xml",
        ]
    },
    {
        "name": "Al Jazeera",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://www.aljazeera.com/xml/rss/all.xml",
        ]
    },
    {
        "name": "Deutsche Welle",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://rss.dw.com/rdf/rss-en-all",
        ]
    },
    {
        "name": "France 24",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://www.france24.com/en/rss",
        ]
    },

    # -------------------------
    # BUSINESS & FINANCE
    # -------------------------
    {
        "name": "Bloomberg",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://feeds.bloomberg.com/politics/news.rss",
            "https://feeds.bloomberg.com/technology/news.rss",
        ],
        "note": "Paywalled — RSS summary only likely; classify on title+summary"
    },
    {
        "name": "CNBC",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://feeds.nbcnews.com/nbcnews/public/business",  # CNBC/NBC business
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",  # Top News
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",   # Markets
            "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19854910",   # Technology
        ]
    },
    {
        "name": "Financial Times",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://www.ft.com/rss/home",
        ],
        "note": "Paywalled — RSS summary only likely"
    },

    # -------------------------
    # TECHNOLOGY
    # -------------------------
    {
        "name": "Ars Technica",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "http://feeds.arstechnica.com/arstechnica/index/",
            "https://feeds.arstechnica.com/arstechnica/features",
            "https://feeds.arstechnica.com/arstechnica/technology-lab",
        ],
        "note": "Free RSS provides excerpts only; full text requires subscription"
    },
    {
        "name": "The Verge",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://www.theverge.com/rss/index.xml",
        ],
        "note": "Free RSS provides excerpts only after 2025 paywall launch"
    },
    {
        "name": "Wired",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://www.wired.com/feed/rss",
        ]
    },
    {
        "name": "TechCrunch",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://techcrunch.com/feed/",
        ]
    },
    {
        "name": "MIT Technology Review",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://www.technologyreview.com/feed/",
        ]
    },

    # -------------------------
    # SCIENCE & HEALTH
    # -------------------------
    {
        "name": "Scientific American",
        "lean": "Center-Left",
        "credibility": "High",
        "feeds": [
            "https://www.scientificamerican.com/platform/syndication/rss/",
        ]
    },
    {
        "name": "STAT News",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://www.statnews.com/feed/",
        ]
    },
    {
        "name": "New Scientist",
        "lean": "Center",
        "credibility": "High",
        "feeds": [
            "https://www.newscientist.com/feed/home/",
        ]
    },
]