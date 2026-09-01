import io
from datetime import UTC, datetime
from uuid import UUID, uuid4

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
    User,
)
from tempo_toolkit.application.outbox import OutboxMessage
from tempo_toolkit.application.storage import StoredObject
from tempo_toolkit.contracts.events import MetadataDeletedEvent, MetadataReadyEvent
from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.common.entities.similarity import Similarity


def create_current_user_service(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> CurrentUserService:
    return CurrentUserService(
        identity_provider=identity_provider,
        authorized_user_finder=authorized_user_finder,
    )


def create_user(id: UserID | None = None) -> User:
    return User(
        id=id or UserID(uuid4()),
        username="listener",
        first_name="Test",
        last_name="User",
        email="listener@example.com",
    )


def create_metadata_ready_event(
    upload_id: UploadURN | None = None,
) -> MetadataReadyEvent:
    return MetadataReadyEvent(
        upload_id=upload_id or UploadURN(uuid4()),
        title="Track title",
        artist="Track artist",
        album="Track album",
        genre="Track genre",
        year="2026",
        content_type="audio/mpeg",
    )


def create_metadata_deleted_event(
    upload_id: UploadURN | None = None,
) -> MetadataDeletedEvent:
    return MetadataDeletedEvent(upload_id=upload_id or UploadURN(uuid4()))


def create_object(body: bytes = b"audio data") -> StoredObject:
    return StoredObject(
        Body=io.BytesIO(body),
        ContentLength=len(body),
        ContentType="audio/mpeg",
    )


def create_outbox_message(id: int, aggregate_id: UUID | None = None) -> OutboxMessage:
    return OutboxMessage(
        id=id,
        aggregate_type="recommendation",
        aggregate_id=str(aggregate_id or uuid4()),
        event_type="rk.tempo.rc.feature.ready",
        payload={},
        created_at=datetime.now(UTC),
    )


def create_similarity(
    point_id: UUID | None = None,
    score: float = 0.9,
) -> Similarity:
    return Similarity(point_id=point_id or uuid4(), score=score)
