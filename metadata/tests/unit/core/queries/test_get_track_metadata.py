from uuid import uuid4

import pytest

from toolkit.service.exceptions import NotFound

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.queries.get_track_metadata import GetTrackMetadata
from app.core.queries.ports.metadata_reader import MetadataReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_metadata_qm,
    create_user,
)


def make_get_track_metadata_query(
    metadata_reader: MetadataReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetTrackMetadata:
    return GetTrackMetadata(
        metadata_reader=metadata_reader,
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
    )


@pytest.mark.asyncio
async def test_get_track_metadata_success(
    metadata_reader: MetadataReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    authorized_user_finder.get_by_id.return_value = create_user()
    upload_id = uuid4()
    expected = create_metadata_qm(id=upload_id)
    metadata_reader.get_by_id.return_value = expected
    query = make_get_track_metadata_query(
        metadata_reader, identity_provider, authorized_user_finder
    )

    result = await query(upload_id)

    assert result is expected
    metadata_reader.get_by_id.assert_called_once_with(upload_id)


@pytest.mark.asyncio
async def test_get_track_metadata_not_found(
    metadata_reader: MetadataReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    authorized_user_finder.get_by_id.return_value = create_user()
    metadata_reader.get_by_id.return_value = None
    query = make_get_track_metadata_query(
        metadata_reader, identity_provider, authorized_user_finder
    )

    with pytest.raises(NotFound):
        await query(uuid4())
