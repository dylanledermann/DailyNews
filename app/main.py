# Main application to run fetch, parse, query, and html generation services
from app.config.database import init_db
from app.helpers.scrapeHelpers import is_blocklisted
from app.repo.articleRepo import ArticleRepo
from app.services.articlePullService import ArticlePullService
from app.services.feedPullService import FeedPullService
from app.services.htmlGenerationService import HTMLGenerationService
from app.services.llmService import LLMService
from app.sources.sources import SOURCES

# Main file to be ran
# Creates db and sets up env
# Orchestrates services 
def main():
    init_db()

    # Get Services
    feedPuller = FeedPullService()
    articlePuller = ArticlePullService()
    llmService = LLMService()
    htmlGenerator = HTMLGenerationService()
    articleRepo = ArticleRepo()

    # Fetch feeds
    articles = feedPuller.fetch_all_sources(SOURCES)
    failed = 0
    skipped = 0
    duped = 0
    for article in articles:

        # Prevent duplication
        if articleRepo.article_exists(article["id"]):
            duped += 1
            continue
        
        # Skip impossible scraping
        skip_scrape = (
            article["body_truncated"] or is_blocklisted(article["url"])
        )
        if skip_scrape:
            skipped += 1
            article["body_truncated"] = 1
            print(f"Skipping scrape for article {article["title"]}")

        else:
            scraped = articlePuller.scrape_article(article["url"])
            article.update(scraped)
        # If no title then failed to fetch article and it should not be included
        if not article["title"] or not article["body"]:
            failed += 1
            continue

        # Classify article
        classification = llmService.classify_article(article)
        if classification:
            article.update(classification)

        # Save article
        articleRepo.upsert_article(article)
    
    removed = articleRepo.cleaup_articles()
    print(f"{removed} Articles Removed")

    # Generate HTML page(s)
    htmlGenerator.generateHtml()
    print(f"failed: {failed}, skipps: {skipped}, duped: {duped}")
    print("\nPipeline Complete.")

if __name__ == "__main__":
    main()