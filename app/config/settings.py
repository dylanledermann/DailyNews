from dotenv import load_dotenv
import os

load_dotenv(".env")

# LLM_API_KEY=
# HTML_GENERATION=
# DB_PATH=
# NEWS_CLEANUP=2 # Days after last update to remove news article
SETTINGS = None

def load_settings():
    global SETTINGS
    SETTINGS = {
        "LLM_BASE_URL": os.getenv("LLM_BASE_URL") or "http://localhost:11434/v1",
        "LLM_API_KEY":os.getenv("LLM_API_KEY") or "",
        "HTML_GENERATION_PATH":os.getenv("HTML_GENERATION_PATH") or "./index.html",
        "DB_PATH":os.getenv("DB_PATH") or "./app/db/news_database.db",
        "NEWS_CLEANUP":int(os.getenv("NEWS_CLEANUP") or '2'),
        "SOURCES_PATH":os.getenv("SOURCES_PATH") or "./app/sources/sources.json",
        "USER_AGENT":os.getenv("USER_AGENT"),
        "DATA_DIRECTORY":os.getenv("DATA_DIRECTORY"),
    }

load_settings()