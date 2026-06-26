import random
from datetime import datetime
from uuid import UUID, uuid4

from faker import Faker
from toolkit.entities import User
from toolkit.types.enum import UploadStatus
from toolkit.types_ import UserID

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.outbox_service import OutboxService
from app.core.common.services.upload_service import UploadService
from app.core.models.upload import Upload


def create_current_user_service(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder
) -> CurrentUserService:
    return CurrentUserService(
        identity_provider=identity_provider,
        authorized_user_finder=authorized_user_finder,
    )


def create_user_id(value: UserID | None = None) -> UserID:
    return value or UserID(uuid4())


def create_username(value: str | None = None) -> str:
    return value or Faker().user_name()


def create_first_name(value: str | None = None) -> str:
    return value or Faker().first_name()


def create_last_name(value: str | None = None) -> str:
    return value or Faker().last_name()


def create_email(value: str | None = None) -> str:
    return value or Faker().email()


def create_user(
    id: UserID | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None
) -> User:
    return User(
        id=id or create_user_id(),
        username=username or create_username(),
        first_name=first_name or create_first_name(),
        last_name=last_name or create_last_name(),
        email=email or create_email()
    )


def create_upload_service() -> UploadService:
    return UploadService()


def create_upload(
    id: UUID | None = None,
    filename: str | None = None,
    content_type: str | None = None,
    size: int | None = None,
    status: UploadStatus | None = None,
    created_by: str | None = None,
    created_at: datetime | None = None,
) -> Upload:
    faker = Faker()
    return Upload(
        id=id or faker.uuid4(),
        filename=filename or faker.file_name(),
        content_type=content_type or faker.mime_type(),
        size=size or faker.random_int(),
        status=status or random.choice(list(UploadStatus)),
        created_by=created_by or faker.uuid4(),
        created_at=created_at or faker.date_time(),
    )


def create_outbox_service(utc_timer: UTCTimer) -> OutboxService:
    return OutboxService(timer=utc_timer)
