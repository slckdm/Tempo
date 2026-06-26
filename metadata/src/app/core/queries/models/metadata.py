
from datetime import datetime

from pydantic import BaseModel


class MetadataQM(BaseModel):
    title: str | None
    artist: str | None
    album: str | None
    genre: str | None
    year: str | None
    duration: float | None
    cover_key: str | None
    size: int
    created_at: datetime
