from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Video
from app.schemas import VideoOut
from typing import List
import asyncio
from app.fetcher import run_fetcher

app = FastAPI(title="YouTube Video Fetcher")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_fetcher())


@app.get("/videos", response_model=List[VideoOut])
def get_videos(
    skip: int = 0, limit: int = Query(10, le=50), db: Session = Depends(get_db)
):
    return (
        db.query(Video)
        .order_by(Video.published_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
