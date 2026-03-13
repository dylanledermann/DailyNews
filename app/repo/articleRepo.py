from app.config.database import get_connection
from app.config.settings import SETTINGS

class ArticleRepo:
    def __init__(self,):
        self.db = get_connection()

    def article_exists(self, article_id: str) -> bool:
        row = self.db.execute(
            "SELECT id FROM articles WHERE id = ?;", 
            (article_id,)
        ).fetchone()
        return row is not None
    
    def upsert_article(self, article: dict) -> str:
        print(article)
        row = self.db.execute("""
            INSERT INTO articles (
                id, title, url, body, body_truncated, published, 
                source_name, source_lean, source_credibility, 
                category, political_lean, bias_score, 
                factuality_score, tone, bias_reasoning, emotional_language,
                summary, classification_raw, classified_at
            ) VALUES (
                :id, :title, :url, :body, :body_truncated, :published,
                :source_name, :source_lean, :source_credibility,
                :category, :political_lean, :bias_score,
                :factuality_score, :tone, :bias_reasoning, :emotional_language,
                :summary, :classification_raw, :classified_at
            )
            ON CONFLICT(id) DO NOTHING
            RETURNING id;
        """, article).fetchone()
        self.db.commit()
        return row["id"]
    
    def get_recent_articles(self, limit: int = 100) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM articles ORDER BY published DESC LIMIT ?;", 
            (limit,)
        ).fetchall()
        return [dict(row) for row in rows]
    
    def cleaup_articles(self) -> int:
        deleted = self.db.execute(
            "DELETE FROM articles WHERE julianday(published) - julianday(date('now')) > ?;",
            (SETTINGS["NEWS_CLEANUP"])
        ).rowcount
        self.db.commit()
        return deleted