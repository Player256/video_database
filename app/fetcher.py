import asyncio
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from app.youtube import YouTubeFetcher
from app.database import SessionLocal
from app.models import Video
from app.config import FETCH_INTERVAL


async def run_fetcher():
    fetcher = YouTubeFetcher()
    last_fetch_time = datetime.utcnow() - timedelta(minutes=5)

    while True:
        print(f"Fetching videos after {last_fetch_time.isoformat()}...")
        videos = await fetcher.fetch_latest_videos(
            published_after=last_fetch_time.isoformat() + "Z"
        )

        session = SessionLocal()
        count = 0
        try:
            for vid in videos:
                try:
                    video = Video(
                        video_id=vid["video_id"],
                        title=vid["title"],
                        description=vid["description"],
                        published_at=vid["published_at"],
                        thumbnail_url=vid["thumbnail_url"],
                    )
                    session.add(video)
                    session.commit()
                    count += 1
                except IntegrityError:
                    session.rollback()
            print(f"Saved {count} new videos to DB")
        except Exception as e:
            print(f"Error saving videos: {e}")
        finally:
            session.close()

        if videos:
            latest_time = max(
                datetime.fromisoformat(v["published_at"].replace("Z", ""))
                for v in videos
            )
            last_fetch_time = max(last_fetch_time, latest_time)

        await asyncio.sleep(FETCH_INTERVAL)
