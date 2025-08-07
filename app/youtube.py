import httpx
from datetime import datetime, timedelta
from app.config import API_KEYS, SEARCH_QUERY

API_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="


class YouTubeFetcher:
    def __init__(self):
        self.api_keys = API_KEYS
        self.index = 0

    def get_key(self):
        return self.api_keys[self.index]

    def rotate_key(self):
        self.index = (self.index + 1) % len(self.api_keys)

    async def fetch_latest_videos(self, published_after: str):
        params = {
            "key": self.get_key(),
            "q": SEARCH_QUERY,
            "part": "snippet",
            "type": "video",
            "order": "date",
            "publishedAfter": published_after,
            "maxResults": 10,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.get(API_ENDPOINT, params=params)
            if resp.status_code == 403:
                self.rotate_key()
                return []
            data = resp.json()

            videos = []
            for item in data.get("items", []):
                snippet = item["snippet"]
                videos.append(
                    {
                        "video_id": item["id"]["videoId"],
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "published_at": snippet["publishedAt"],
                        "thumbnail_url": snippet["thumbnails"]["high"]["url"],
                    }
                )
            return videos
