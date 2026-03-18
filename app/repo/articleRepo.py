from app.config.database import get_connection
from app.config.settings import SETTINGS

class ArticleRepo:
    def __init__(self,):
        """Initiate ArticleRepo object."""
        self.db = get_connection()

    def article_exists(self, article_id: str) -> bool:
        """
        Checks if the given article ID exists in the database.

        Args:
            article_id (str): Article ID to be checked.

        Returns:
            bool: True if the article ID exists in the database, False otherwise.
        """
        row = self.db.execute(
            "SELECT id FROM articles WHERE id = ?;", 
            (article_id,)
        ).fetchone()
        return row is not None
    
    def upsert_article(self, article: dict) -> str:
        """
        Inserts the article into the database. If there is a conflict, nothing happens.

        Args:
            article (dict): Article to be inserted into the database.

        Returns:
            str: The ID of the article inserted.
        """
        row = self.db.execute("""
            INSERT INTO articles (
                id, title, url, body, body_truncated, published, 
                source_name, source_lean, source_credibility, 
                category, political_lean, bias_score, 
                factuality_score, tone, bias_reasoning, emotional_language,
                summary, summary_ai, classification_raw, classified_at
            ) VALUES (
                :id, :title, :url, :body, :body_truncated, :published,
                :source_name, :source_lean, :source_credibility,
                :category, :political_lean, :bias_score,
                :factuality_score, :tone, :bias_reasoning, :emotional_language,
                :summary, :summary_ai, :classification_raw, :classified_at
            )
            ON CONFLICT(id) DO NOTHING
            RETURNING id;
        """, 
            article
        ).fetchone()
        self.db.commit()
        return row["id"]
    
    def get_recent_articles(self) -> list[dict]:
        """
        Gets all recent articles from the database in descending order (newest first).

        Returns:
            list[dict]: List of articles in the database.
        """
        rows = self.db.execute(
            "SELECT * FROM articles ORDER BY published DESC;"
        ).fetchall()
        return [dict(row) for row in rows]
    
    def cleaup_articles(self) -> int:
        """
        Cleans the database of outdated articles.

        Returns:
            int: number of articles deleted.
        """
        deleted = self.db.execute(
            "DELETE FROM articles WHERE julianday(published) - julianday(date('now')) > ?;",
            (SETTINGS["NEWS_CLEANUP"],)
        ).rowcount
        self.db.commit()
        return deleted