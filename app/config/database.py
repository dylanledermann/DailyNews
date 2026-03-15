import sqlite3

from app.config.settings import SETTINGS

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    body TEXT NOT NULL,
    body_truncated INTEGER DEFAULT 0,
    published TEXT,
    source_name TEXT,
    source_lean TEXT,
    source_credibility TEXT,
    category TEXT,
    political_lean TEXT,
    bias_score REAL,
    factuality_score REAL,
    tone TEXT,
    bias_reasoning TEXT,
    emotional_language INTEGER DEFAULT 0,
    summary TEXT,
    summary_ai TEXT,
    classification_raw TEXT,
    classified_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_published ON articles(published);
CREATE INDEX IF NOT EXISTS idx_source ON articles(source_name);
CREATE INDEX IF NOT EXISTS idx_category ON articles(category);
"""

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(SETTINGS["DB_PATH"])
    conn.row_factory = sqlite3.Row # rows behave like dicts
    conn.execute("PRAGMA journnal_mode=WAL") # safer concurrect reads
    return conn

def init_db() -> sqlite3.Connection:
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    return conn