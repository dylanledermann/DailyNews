# Pulls, formats, and stores news sources in a SQLite db
import feedparser
import hashlib
import requests
import time
from datetime import datetime
from googlenewsdecoder import gnewsdecoder
from tqdm import tqdm

from app.helpers.scrapeHelpers import check_truncation, clean_text

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

PAYWALL_SIGNALS = {
    "subscribe to read",
    "subscription required",
    "sign in to read",
    "become a member",
    "this article is for subscribers",
    "to continue reading",
    "read the full article",
    "unlock this story",
    "premium content",
}

PAYWALLED_LENGTH = 200

class FeedPullService:
    # Url Resolution (Google News redirect -> real URL)
    def resolve_google_url(self, google_url: str) -> str | None:
        """
        Google News RSS entries wrap real article URLs in a redirect.
        Use googlenewsdecoder package to decode article URL.
        """
        try:
            result = gnewsdecoder(google_url, interval=2)
            if result.get("status"):
                return result["decoded_url"]
            print(f"Decoder returned error: {result.get('message')}")
            return None
        except requests.RequestException as e:
            print(f"URL resolution failed: {google_url - {e}}")
            return None
            
    def make_article_id(self, url: str) -> str:
        """Stable unique ID derived from canonical article URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def parse_entry(self, entry: feedparser.FeedParserDict, source: dict, resolved_url: str) -> dict:
        """
        Normalize a feedparser entry into a flat article dict.
        Body and classification fields are null - filled by scraper/classifier later.
        """
        url = resolved_url or entry.get("link", "")

        published = ""
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6]).isoformat()
        elif entry.get("published"):
            published = entry["published"]
        else:
            published = datetime.now().isoformat()
        
        # Clean all extracted text
        cleanedSummary = clean_text(entry.get("summary", "").strip())
        cleanedTitle = clean_text(entry.get("title", "").strip())
        return {
            # Core identity
            "id": self.make_article_id(url),
            "title": cleanedTitle,
            "url": url,
            "summary": cleanedSummary,
            "published": published,
            # Source metadata (pre-tagged, not AI-inferred)
            "source_name": source["name"],
            "source_lean": source.get("lean", "Unknown"),
            "source_credibility": source.get("credibility", "Unknown"),
            # Body - filled by scraper
            "body": None,
            "body_truncated": 0,
            # Classification - filled by classifier
            "category": None,
            "political_lean": None,
            "bias_score": None,
            "factuality_score": None,
            "tone": None,
            "bias_reasoning": None,
            "emotional_language": None,
            "summary_ai": None,
            "classification_raw": None,
            "classified_at":None,
        }
    
    def fetch_feed(self, feed_url: str, source: dict, is_google_news: bool = False) -> list[dict]:
        """
        Fetch and parse a single RSS/Atom feed URL.
        If is_google_news=True, resolve redirect URLs before storing.
        """
        print(f"Fetching: {feed_url}")

        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"feedparser failed: {e}")
            return []

        if feed.bozo and not feed.entries:
            print(f"Feed parse error (bozo): {feed.bozo_exception}")
            return []
        
        articles = []

        for entry in feed.entries:
            raw_url = entry.get("link", "")
            if not raw_url:
                continue
                
            if is_google_news:
                resolved_url = self.resolve_google_url(raw_url)
                if not resolved_url:
                    print(f"Could not resolve: {raw_url}")
                    continue
                time.sleep(0.5)
            else:
                resolved_url = raw_url
            
            article = self.parse_entry(entry, source, resolved_url)

            if not article["url"] or not article["title"]:
                continue
            
            articles.append(article)

        print(f"{len(articles)} articles from {source['name']}")
        return articles
    
    def fetch_all_sources(self, sources: list[dict]) -> list[dict]:
        """
        Iterate all sources and their feeds.
        Returns a flat deduplicated list of article dicts
        with body_truncated set where detectable at feed level.
        """
        all_articles = []
        seen_ids = set()

        for i in tqdm(range(len(sources))):
            source = sources[i]
            print(f"\n[{source['name']}]")
            feed_type = source.get("feed_type", "rss")
            is_google_news = feed_type == "google_news"

            for feed_url in source.get("feeds", []):
                articles = self.fetch_feed(feed_url, source, is_google_news)

                for article in articles:
                    if article["id"] in seen_ids:
                        continue

                    seen_ids.add(article["id"])

                    # RSS summary can give an early truncation signal
                    # flag summary for paywall language early
                    if check_truncation(article["url"], article["summary"]):
                        article["body_truncated"] = 1

                    all_articles.append(article)

                time.sleep(1)

        print(f"\n Fetched {len(all_articles)} unique articles across all sources")
        return all_articles
    
def test_source(source: dict):
    """Quick diagnostic to verify a source's feeds are working."""
    print(f"\n=== Testing: {source['name']} ===")
    service = FeedPullService()
    articles = service.fetch_all_sources([source])
    for a in articles[:3]:
        print(f"  Title:          {a['title'][:70]}")
        print(f"  URL:            {a['url'][:70]}")
        print(f"  Published:      {a['published']}")
        print(f"  Body truncated: {bool(a['body_truncated'])}")
        print()

if __name__ == "__main__":
    from app.sources.sources import SOURCES
    test_source(SOURCES[0])