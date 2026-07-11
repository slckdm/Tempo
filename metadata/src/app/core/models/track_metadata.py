from datetime import datetime
from uuid import UUID

from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType


class TrackMetadata:
    def __init__(
        self,
        *,
        upload_id: UUID,
        title: str | None = None,
        artist: str | None = None,
        album: str | None = None,
        albumartist: str | None = None,
        genre: str | None = None,
        year: str | None = None,
        track_number: int | None = None,
        disc: int | None = None,
        duration: float | None = None,
        bitrate: float | None = None,
        samplerate: int | None = None,
        channels: int | None = None,
        comment: str | None = None,
        cover_key: str | None = None,
        processing_status: UploadStatus,
        error: str | None = None,
        filename: str,
        content_type: str,
        size: int,
        created_by: UUID,
        created_at: datetime,
        origin_upload_status: UploadStatus,
        updated_at: datetime,
    ) -> None:
        self.upload_id = upload_id
        self.title = title
        self.artist = artist
        self.album = album
        self.albumartist = albumartist
        self.genre = genre
        self.year = year
        self.track_number = track_number
        self.disc = disc
        self.duration = duration
        self.bitrate = bitrate
        self.samplerate = samplerate
        self.channels = channels
        self.comment = comment
        self.cover_key = cover_key
        self.processing_status = processing_status
        self.error = error
        self.filename = filename
        self.content_type = content_type
        self.size = size
        self.created_by = created_by
        self.created_at = created_at
        self.origin_upload_status = origin_upload_status
        self.updated_at = updated_at

    @property
    def urn(self) -> UploadURNType:
        return UploadURNType(id=self.upload_id)
