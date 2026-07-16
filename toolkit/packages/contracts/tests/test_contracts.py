"""Cross-service contract tests."""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel

from tempo_toolkit.contracts.events import UploadCompletedEvent
from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.routing import UPLOAD_COMPLETED_EVENT_RK
from tempo_toolkit.contracts.uploads import UploadStatus, UploadURN


class UploadModel(BaseModel):
    """Pydantic model containing an upload URN."""

    upload_id: UploadURN


def test_upload_urn_round_trip() -> None:
    """Upload URNs retain their wire representation through Pydantic."""
    upload_id = uuid4()
    value = f"urn:mng.upload:{upload_id}"
    model = UploadModel.model_validate({"upload_id": value})

    assert model.upload_id.id == str(upload_id)
    assert model.model_dump(mode="json") == {"upload_id": value}


def test_upload_event_wire_shape() -> None:
    """Upload events keep their stable field names and values."""
    upload_id = UploadURN(uuid4())
    event = UploadCompletedEvent(
        upload_id=upload_id,
        s3_key=str(upload_id),
        filename="track.mp3",
        content_type="audio/mpeg",
        size=10,
        created_by=UserID(uuid4()),
        created_at=datetime.now(UTC),
        status=UploadStatus.PROCESSING,
    )

    payload = event.model_dump(mode="json")
    assert payload["upload_id"] == str(upload_id)
    assert payload["schema_version"] == 1
    assert payload["status"] == "PROCESSING"


def test_routing_key_is_unchanged() -> None:
    """Routing keys retain their broker wire value."""
    assert str(UPLOAD_COMPLETED_EVENT_RK) == "rk.tempo.mng.upload.completed"
