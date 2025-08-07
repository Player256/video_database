from pydantic import BaseModel
from datetime import datetime


class VideoOut(BaseModel):
    video_id: str
    title: str
    description: str
    published_at: datetime
    thumbnail_url: str

    class Config:
        orm_mode = True
