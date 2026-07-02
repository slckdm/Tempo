import io
from typing import Sequence
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.security import OAuth2

from faker import Faker

from toolkit.entities.object import Object
from toolkit.types.urn import UploadURNType

from app.core.common.auth.service import AuthorizationService
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.queries.ports.object_storage import ObjectStorage
from app.core.queries.stream import Stream

faker = Faker()


def create_stream(object_storage: ObjectStorage, identity: IdentityProvider) -> Stream:
    return Stream(object_storage=object_storage, identity=identity)


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
