from time import sleep

from app.helpers.scrapeHelpers import check_truncation, extract_metadata, get_domain, is_blocklisted
import trafilatura
import requests
from bs4 import BeautifulSoup

from app.services.llmService import LLMService

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

class ArticlePullService:

    def extract_via_trafilatura(self, html: str) -> str | None:
        """
        Strategy 1: Trafilatura — purpose-built article extractor.
        Best general-purpose option, handles most news sites well.
        """
        text = trafilatura.extract(
            html,
            include_comments = False,
            include_tables = False,
            no_fallback = False,
            favor_precision = True, # prefer less text over noisy text
        )

        if text and len(text.split()) > 100:
            return text
        return None
    
    def extract_via_article_tag(self, soup: BeautifulSoup) -> str | None:
        """
        Strategy 2: Semantic <article> tag.
        Reuters, BBC, AP, and most modern news sites use this.
        """
        article_tag = soup.find("article")
        if article_tag:
            paragraphs = article_tag.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)
            if len(text.split()) > 100:
                return text
        return None
    
    def extract_via_content_divs(self, soup: BeautifulSoup) -> str | None:
        """
        Strategy 3: Common content div class names.
        Fallback for sites that don't use <article> tags.
        """
        CONTENT_SELECTORS = [
            "article-body",
            "story-body",
            "post-content",
            "entry-content",
            "article-content",
            "main-content",
            "article__body",
            "story__body",
            "RichTextStoryBody",     # Reuters-specific
            "article-body__content", # Guardian-specific
        ]

        for selector in CONTENT_SELECTORS:
            div = soup.find("div", class_=lambda c: c and selector.lower() in c.lower())
            if div:
                paragraphs = div.find_all('p')
                text = " ".join(p.get_text(strip=True) for p in paragraphs)
                if len(text.split()) > 100:
                    return text
        return None
    
    def extract_via_density(self, soup: BeautifulSoup) -> str | None:
        """
        Strategy 4: Paragraph density fallback.
        Find the div with the most <p> tags — usually the article body.
        Last resort, least precise.
        """
        all_divs = soup.find_all("div")
        if all_divs:
            best = max(all_divs, key = lambda d: len(d.find_all("p")))
            paragraphs = best.find_all("p")
            text = " ".join(p.get_text(strip=True) for p in paragraphs)
            if len(text.split()) > 100:
                return text
        return None

    def scrape_article(self, url: str) -> dict:
        """
        Fetch and extract the full article body from a URL.

        Returns a dict with:
            body          — extracted article text (None if failed)
            body_truncated — 1 if paywalled/truncated, 0 if full
            scrape_method  — which strategy succeeded (for diagnostics)
            author         — from meta tags
            published      — from meta tags (may refine RSS publish date)
            description    — og:description / meta description
            og_image       — article thumbnail URL
            section        — article:section meta tag
            keywords       — meta keywords
        """
        result = {
            "body":           None,
            "body_truncated": 0,
            "scrape_method":  None,
            "author":         None,
            "published":      None,
            "description":    None,
            "og_image":       None,
            "section":        None,
            "keywords":       None,
        }

        if is_blocklisted(url):
            print(f"Blocklisted {get_domain(url)}")
            result["body_truncated"] = 1
            return result
        
        # HTTP Get - ensure it goes through
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            html = response.text
        except requests.HTTPError as e:
            print(f"HTTP Error for {url}: {e}")
            return result
        except requests.RequestException as e:
            print(f"Request Exception for {url}: {e}")
            return result
        finally:
            sleep(1) # Crawl delay

        # Extract metadata
        soup = BeautifulSoup(html, "html.parser")
        # Remove noise/unneeded tags
        for tag in soup(["script", "style", "nav", "footer",
            "header", "aside", "iframe", "noscript",
            "figure", "figcaption", "button", "form"
        ]):
            tag.decompose()
        metadata = extract_metadata(soup)
        result.update({k:v for k, v in metadata.items() if v is not None})

        # Extract body
        strategies = [
            ("trafilatura", lambda: self.extract_via_trafilatura(html)),
            ("article_tag", lambda: self.extract_via_article_tag(soup)),
            ("content_divs", lambda: self.extract_via_content_divs(soup)),
            ("density", lambda: self.extract_via_density(soup)),
        ]

        for strategy, method in strategies:
            try:
                text = method()
                if text:
                    result["body"] = text
                    result["scrape_method"] = strategy
                    break
            except Exception as e:
                print(f"Error occurred on strategy {strategy}: {e}")
        
        if not result["body"]:
            print(f"Unable to get body: {url}")

        result["body_truncated"] = check_truncation(url, result["body"])
        
        return result
    
def test_scrape(url: str):
    print(f"=== Scraping {url} ===")
    aps = ArticlePullService()
    result = aps.scrape_article(url)
    print(f"  Method:    {result['scrape_method']}")
    print(f"  Truncated: {bool(result['body_truncated'])}")
    print(f"  Author:    {result['author']}")
    print(f"  Published: {result['published']}")
    print(f"  Keywords:  {result['keywords']}")
    print(f"  Body ({len((result['body'] or '').split())} words):")
    print(f"  {(result['body'] or '')[:300]}...")

if __name__ == "__main__":
    test_scrape("https://apnews.com/article/iran-israel-us-march-12-2026-oil-prices-90e17dbf7354d1e9428994ab2a036506")