from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    description = Column(Text)
    published_at = Column(DateTime, index=True)
    thumbnail_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
