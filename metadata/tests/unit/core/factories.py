import io
from datetime import UTC, datetime
from uuid import UUID, uuid4

from faker import Faker

from toolkit.entities import User
from toolkit.entities.object import Object
from toolkit.messaging.contracts import UploadCompletedEvent, UploadDeletedEvent
from toolkit.types.enum import UploadStatus
from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID

from app.core.common.entities.metadata import Cover, Metadata
from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.metadata_service import MetadataService
from app.core.common.services.outbox_service import OutboxService
from app.core.models.outbox_message import OutboxMessage
from app.core.models.track_metadata import TrackMetadata
from app.core.queries.models.list_metadata import ListMetadataQM
from app.core.queries.models.metadata import MetadataQM
from app.core.queries.ports.metadata_reader import FilterParams
from app.core.queries.schemas.pagination import PaginationParams

faker = Faker()


def create_current_user_service(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> CurrentUserService:
    return CurrentUserService(
        identity_provider=identity_provider,
        authorized_user_finder=authorized_user_finder,
    )


def create_metadata_service(utc_timer: UTCTimer) -> MetadataService:
    return MetadataService(utc_timer=utc_timer)


def create_outbox_service(utc_timer: UTCTimer) -> OutboxService:
    return OutboxService(timer=utc_timer)


def create_user_id(value: UserID | None = None) -> UserID:
    return value or UserID(uuid4())


def create_user(
    id: UserID | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> User:
    return User(
        id=id or create_user_id(),
        username=username or faker.user_name(),
        first_name=first_name or faker.first_name(),
        last_name=last_name or faker.last_name(),
        email=email or faker.email(),
    )


def create_cover(
    data: bytes | None = None,
    mime_type: str | None = "image/png",
) -> Cover:
    return Cover(data=data or faker.binary(length=16), mime_type=mime_type)


def create_metadata(
    title: str | None = None,
    artist: str | None = None,
    cover: Cover | None = None,
) -> Metadata:
    return Metadata(
        title=title or faker.sentence(nb_words=3),
        artist=artist or faker.name(),
        album=faker.sentence(nb_words=2),
        genre=faker.word(),
        year=str(faker.year()),
        duration=faker.pyfloat(positive=True),
        cover=cover,
    )


def create_upload_completed_event(
    upload_id: UploadURNType | None = None,
    s3_key: str | None = None,
    filename: str | None = None,
    content_type: str | None = None,
    size: int | None = None,
    created_by: UserID | None = None,
    created_at: datetime | None = None,
    status: UploadStatus = UploadStatus.PROCESSING,
) -> UploadCompletedEvent:
    return UploadCompletedEvent(
        upload_id=upload_id or UploadURNType(uuid4()),
        s3_key=s3_key or str(uuid4()),
        filename=filename or faker.file_name(extension="mp3"),
        content_type=content_type or "audio/mpeg",
        size=size or faker.random_int(),
        created_by=created_by or create_user_id(),
        created_at=created_at or datetime.now(UTC),
        status=status,
    )


def create_upload_deleted_event(
    upload_id: UploadURNType | None = None,
    s3_key: str | None = None,
) -> UploadDeletedEvent:
    return UploadDeletedEvent(
        upload_id=upload_id or UploadURNType(uuid4()),
        s3_key=s3_key or str(uuid4()),
    )


def create_track_metadata(
    upload_id: UUID | None = None,
    cover_key: str | None = None,
    processing_status: UploadStatus = UploadStatus.COMPLETED,
) -> TrackMetadata:
    now = datetime.now(UTC)
    return TrackMetadata(
        upload_id=upload_id or uuid4(),
        title=faker.sentence(nb_words=3),
        artist=faker.name(),
        album=faker.sentence(nb_words=2),
        albumartist=None,
        genre=faker.word(),
        year=str(faker.year()),
        track_number=None,
        disc=None,
        duration=faker.pyfloat(positive=True),
        bitrate=None,
        samplerate=None,
        channels=None,
        comment=None,
        cover_key=cover_key,
        processing_status=processing_status,
        error=None,
        filename=faker.file_name(extension="mp3"),
        content_type="audio/mpeg",
        size=faker.random_int(),
        created_by=uuid4(),
        created_at=now,
        origin_upload_status=UploadStatus.PROCESSING,
        updated_at=now,
    )


def create_object(
    body: bytes | None = None,
    content_type: str = "audio/mpeg",
) -> Object:
    data = body if body is not None else faker.binary(length=32)
    return Object(
        Body=io.BytesIO(data),
        ContentLength=len(data),
        ContentType=content_type,
    )


def create_outbox_message(
    id: int | None = None,
    aggregate_id: UUID | None = None,
) -> OutboxMessage:
    return OutboxMessage(
        id=id if id is not None else faker.random_int(),
        aggregate_type="metadata",
        aggregate_id=aggregate_id or uuid4(),
        event_type="rk.tempo.md.metadata.ready",
        payload={},
        created_at=datetime.now(UTC),
    )


def create_metadata_qm(
    id: UUID | None = None,
    processing_status: UploadStatus = UploadStatus.COMPLETED,
) -> MetadataQM:
    return MetadataQM(
        id=id or uuid4(),
        filename=faker.file_name(extension="mp3"),
        content_type="audio/mpeg",
        processing_status=processing_status,
        title=faker.sentence(nb_words=3),
        artist=faker.name(),
        album=faker.sentence(nb_words=2),
        genre=faker.word(),
        year=str(faker.year()),
        duration=faker.pyfloat(positive=True),
        cover_key=None,
        size=faker.random_int(),
        created_at=datetime.now(UTC),
    )


def create_list_metadata_qm(
    metadata: list[MetadataQM] | None = None,
    total: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> ListMetadataQM:
    items = metadata if metadata is not None else [create_metadata_qm()]
    return ListMetadataQM(
        metadata=items,
        total=total if total is not None else len(items),
        limit=limit,
        offset=offset,
    )


def create_filter_params(
    title: str | None = None,
    artist: str | None = None,
    album: str | None = None,
    genre: str | None = None,
) -> FilterParams:
    return FilterParams(title=title, artist=artist, album=album, genre=genre)


def create_pagination_params(offset: int = 0, limit: int = 100) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)
