from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Domains known to block scrapers even with spoofed headers
SCRAPE_BLOCKLIST = [
    "wsj.com",
    "ft.com",
    "bloomberg.com",
    "nytimes.com",
    "theatlantic.com",
    "technologyreview.com",
]

PAYWALLED_DOMAINS = [
    "wsj.com", "ft.com", "bloomberg.com", "nytimes.com",
    "theatlantic.com", "technologyreview.com",
    "theverge.com", "arstechnica.com",
]

PAYWALL_SIGNALS = [
    "subscribe to read",
    "subscription required",
    "sign in to read",
    "become a member",
    "this article is for subscribers",
    "to continue reading",
    "read the full article",
    "unlock this story",
    "premium content",
]

PAYWALLED_LENGTH = 150

def check_truncation(url: str, body: str | None) -> int:
    """
    Detects whether article body is paywalled or truncated.
    Returns 1 if truncated, 0 if fully body available.
    """
    if not body:
            return 1
    body_lower = body.lower()
    if (any(d in get_domain(url) for d in PAYWALLED_DOMAINS) or any(signal in body_lower for signal in PAYWALL_SIGNALS)) and len(body.split()) <= PAYWALLED_LENGTH:
        return 1
    return 0

def get_domain(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")

def is_blocklisted(url: str) -> bool:
    domain = get_domain(url)
    return any(blocked in domain for blocked in SCRAPE_BLOCKLIST)

def extract_metadata(soup: BeautifulSoup):
    """
    Pull structured metadata from <meta> tags.
    These are consistent across almost all news sites.
    """
    def get_meta(prop: str = None, name: str = None) -> str | None:
        tag = None
        if prop:
            tag = soup.find("meta", {"property": prop})
        if not tag and name:
            tag = soup.find("meta", {"name": name})
        return tag["content"].strip() if tag and tag.get("content") else None
    
    return {
        "author":       get_meta(name="author") or get_meta(prop="article:author"),
        "published":    get_meta(prop="article:published_time"),
        "modified":     get_meta(prop="article:modified_time"),
        "description":  get_meta(prop="og:description") or get_meta(name="description"),
        "og_title":     get_meta(prop="og:title"),
        "og_image":     get_meta(prop="og:image"),
        "section":      get_meta(prop="article:section"),
        "keywords":     get_meta(name="keywords"),
    }