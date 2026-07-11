import io
from typing import Sequence
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.security import OAuth2

from faker import Faker

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.object_storage import ObjectStorage
from toolkit.common.services.authorization_service import AuthorizationService
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.entities.object import Object
from toolkit.types.urn import UploadURNType

from app.core.queries.stream import Stream

faker = Faker()


def create_stream(
    object_storage: ObjectStorage, current_user_service: CurrentUserService
) -> Stream:
    return Stream(object_storage=object_storage, current_user_service=current_user_service)


def create_upload_urn(id: UUID | None = None) -> UploadURNType:
    return UploadURNType(id or uuid4())


def create_object(
    body: bytes | None = None,
    content_type: str = "audio/mpeg",
    content_range: str | None = None,
    content_length: int | None = None,
) -> Object:
    data = body if body is not None else faker.binary(length=64)
    return Object(
        Body=io.BytesIO(data),
        ContentLength=content_length if content_length is not None else len(data),
        ContentType=content_type,
        ContentRange=content_range,
    )


def create_authorization_service(
    request: Request, schemas: Sequence[OAuth2]
) -> AuthorizationService:
    return AuthorizationService(request=request, schemas=list(schemas))


def create_current_user_service(
    identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
) -> CurrentUserService:
    return CurrentUserService(
        identity_provider=identity_provider,
        authorized_user_finder=authorized_user_finder,
    )
