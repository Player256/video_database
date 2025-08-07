import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/youtube_db"
)
API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(",")  
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "cricket")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 10))  
