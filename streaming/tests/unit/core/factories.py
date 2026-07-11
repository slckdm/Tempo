import io
from typing import Sequence
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.security import OAuth2

from faker import Faker

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
    User,
)
from tempo_toolkit.application.storage import ObjectStorage, StoredObject
from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadURN
from tempo_toolkit.infrastructure.web import FastAPITokenProvider

from app.core.queries.stream import Stream

faker = Faker()


def create_stream(
    object_storage: ObjectStorage, current_user_service: CurrentUserService
) -> Stream:
    return Stream(object_storage=object_storage, current_user_service=current_user_service)


def create_upload_urn(id: UUID | None = None) -> UploadURN:
    return UploadURN(id or uuid4())


def create_object(
    body: bytes | None = None,
    content_type: str = "audio/mpeg",
    content_range: str | None = None,
    content_length: int | None = None,
) -> StoredObject:
    data = body if body is not None else faker.binary(length=64)
    return StoredObject(
        Body=io.BytesIO(data),
        ContentLength=content_length if content_length is not None else len(data),
        ContentType=content_type,
        ContentRange=content_range,
    )


def create_authorization_service(
    request: Request, schemas: Sequence[OAuth2]
) -> FastAPITokenProvider:
    return FastAPITokenProvider(request=request, schemas=list(schemas))


def create_current_user_service(
    identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
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
