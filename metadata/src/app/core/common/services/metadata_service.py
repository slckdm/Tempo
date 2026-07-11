from datetime import UTC

from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.messaging.contracts import UploadCompletedEvent
from toolkit.types.enum import UploadStatus

from app.core.common.entities.metadata import Metadata
from app.core.models.track_metadata import TrackMetadata


class MetadataService:

    def __init__(
        self, utc_timer: UTCTimer
    ) -> None:
        self._utc_timer = utc_timer

    async def create(self, data: Metadata, upload_data: UploadCompletedEvent) -> TrackMetadata:
        return TrackMetadata(
            upload_id=upload_data.upload_id.id,
            title=data.title,
            artist=data.artist,
            album=data.album,
            albumartist=data.albumartist,
            genre=data.genre,
            year=data.year,
            track_number=data.track,
            disc=data.disc,
            duration=data.duration,
            bitrate=data.bitrate,
            samplerate=data.samplerate,
            channels=data.channels,
            comment=data.comment,
            processing_status=UploadStatus.COMPLETED,
            error=None,
            filename=upload_data.filename,
            content_type=upload_data.content_type,
            size=upload_data.size,
            created_by=upload_data.created_by,
            created_at=upload_data.created_at.astimezone(UTC),
            origin_upload_status=upload_data.status,
            updated_at=self._utc_timer.now,
        )

    async def update_cover_key(self, metadata: TrackMetadata, cover_key: str) -> None:
        metadata.cover_key = cover_key

    async def mark_failed(self, metadata: TrackMetadata, message: str) -> None:
        metadata.error = message
        metadata.processing_status = UploadStatus.FAILED
