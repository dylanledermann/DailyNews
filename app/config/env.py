from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv(".env")

# LLM_API_KEY=
# HTML_GENERATION=
# DB_PATH=
# NEWS_CLEANUP=2 # Days after last update to remove news article
SETTINGS = None

def load_settings():
    SETTINGS = {
        "LLM_API_KEY":os.getenv("LLM_API_KEY"),
        "HTML_GENERATION_PATH":os.getenv("HTML_GENERATION_PATH") or "./app/docs",
        "DB_PATH":os.getenv("DB_PATH") or "./app/db",
        "NEWS_CLEANUP":int(os.getenv("NEWS_CLEANUP")) or 2,
    }
    assert(SETTINGS["LLM_API_KEY"] is not None)