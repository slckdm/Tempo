import pytest

from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.types.enum import UploadStatus

from app.core.models import TrackMetadata
from tests.unit.core.factories import (
    create_metadata,
    create_metadata_service,
    create_track_metadata,
    create_upload_completed_event,
)
from tests.unit.core.mock_types import FROZEN_NOW


@pytest.mark.asyncio
async def test_create_maps_fields(utc_timer: UTCTimer) -> None:
    metadata_service = create_metadata_service(utc_timer)
    data = create_metadata(title="Song", artist="Artist")
    event = create_upload_completed_event()

    metadata = await metadata_service.create(data, event)

    assert isinstance(metadata, TrackMetadata)
    assert metadata.upload_id == event.upload_id.id
    assert metadata.title == "Song"
    assert metadata.artist == "Artist"
    assert metadata.filename == event.filename
    assert metadata.size == event.size
    assert metadata.created_by == event.created_by
    assert metadata.processing_status == UploadStatus.COMPLETED
    assert metadata.error is None
    assert metadata.updated_at == FROZEN_NOW


@pytest.mark.asyncio
async def test_update_cover_key(utc_timer: UTCTimer) -> None:
    metadata_service = create_metadata_service(utc_timer)
    metadata = create_track_metadata(cover_key=None)

    await metadata_service.update_cover_key(metadata, "covers/key")

    assert metadata.cover_key == "covers/key"


@pytest.mark.asyncio
async def test_mark_failed(utc_timer: UTCTimer) -> None:
    metadata_service = create_metadata_service(utc_timer)
    metadata = create_track_metadata(processing_status=UploadStatus.COMPLETED)

    await metadata_service.mark_failed(metadata, "boom")

    assert metadata.processing_status == UploadStatus.FAILED
    assert metadata.error == "boom"
