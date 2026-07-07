import io

import pytest

from toolkit.service.exceptions import NotFound

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.services.current_user_service import CurrentUserService
from app.core.queries.ports.object_storage import ObjectStorage
from app.core.queries.stream import _iter_chunks
from app.outbound.exceptions import StorageError
from tests.unit.core.factories import create_object, create_stream, create_upload_urn, create_current_user_service


def make_current_user_service(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder | None
) -> CurrentUserService:
    return create_current_user_service(
        identity_provider=identity_provider, authorized_user_finder=authorized_user_finder
    )


@pytest.mark.asyncio
async def test_stream_audio_success(
    object_storage: ObjectStorage,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    body = b"audio-bytes-payload"
    object_storage.get_object.return_value = create_object(body=body, content_type="audio/mpeg")
    urn = create_upload_urn()
    current_user_service = make_current_user_service(identity_provider, authorized_user_finder)
    stream = create_stream(object_storage, current_user_service)

    result = await stream(urn, None)

    identity_provider.get_current_user_id.assert_called_once()
    authorized_user_finder.get_by_id.assert_called_once()
    object_storage.get_object.assert_called_once_with(str(urn))
    assert result.content_type == "audio/mpeg"
    assert result.content_range is None
    assert result.content_length == len(body)
    assert b"".join(result.chunks) == body


@pytest.mark.asyncio
async def test_stream_cover_uses_cover_key(
    identity_provider: IdentityProvider,
    object_storage: ObjectStorage,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    object_storage.get_object.return_value = create_object()
    urn = create_upload_urn()
    current_user_service = make_current_user_service(identity_provider, authorized_user_finder)
    stream = create_stream(object_storage, current_user_service)

    await stream(urn, None, cover=True)

    object_storage.get_object.assert_called_once_with(f"covers/{urn}")


@pytest.mark.asyncio
async def test_stream_forwards_range_header(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    object_storage: ObjectStorage,
) -> None:
    object_storage.get_object.return_value = create_object(content_range="bytes 0-9/100")
    urn = create_upload_urn()
    current_user_service = make_current_user_service(identity_provider, authorized_user_finder)
    stream = create_stream(object_storage, current_user_service)

    result = await stream(urn, "bytes=0-9")

    object_storage.get_object.assert_called_once_with(str(urn), Range="bytes=0-9")
    assert result.content_range == "bytes 0-9/100"


@pytest.mark.asyncio
async def test_stream_missing_object_raises_not_found(
    identity_provider: IdentityProvider,
    object_storage: ObjectStorage,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    object_storage.get_object.side_effect = StorageError
    current_user_service = make_current_user_service(identity_provider, authorized_user_finder)
    stream = create_stream(object_storage, current_user_service)

    with pytest.raises(NotFound):
        await stream(create_upload_urn(), None)


def test_iter_chunks_splits_and_stops() -> None:
    chunks = list(_iter_chunks(io.BytesIO(b"abcdef"), chunk_size=2))

    assert chunks == [b"ab", b"cd", b"ef"]


def test_iter_chunks_empty_source() -> None:
    assert list(_iter_chunks(io.BytesIO(b""))) == []
