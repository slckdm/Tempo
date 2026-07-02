import pytest

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.ports.utc_timer import UTCTimer
from app.core.queries.get_tracks_metadata import GetTracksMetadata
from app.core.queries.ports.metadata_reader import MetadataReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_filter_params,
    create_list_metadata_qm,
    create_metadata_service,
    create_pagination_params,
    create_user,
)


def make_get_tracks_metadata_query(
    metadata_reader: MetadataReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
) -> GetTracksMetadata:
    return GetTracksMetadata(
        metadata_service=create_metadata_service(utc_timer),
        metadata_reader=metadata_reader,
        current_user_service=create_current_user_service(
            identity_provider, authorized_user_finder
        ),
    )


@pytest.mark.asyncio
async def test_get_tracks_metadata_success(
    metadata_reader: MetadataReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    utc_timer: UTCTimer,
) -> None:
    authorized_user_finder.get_by_id.return_value = create_user()
    expected = create_list_metadata_qm()
    metadata_reader.list_by_filter.return_value = expected
    filters = create_filter_params(artist="Artist")
    pagination = create_pagination_params(offset=0, limit=50)
    query = make_get_tracks_metadata_query(
        metadata_reader, identity_provider, authorized_user_finder, utc_timer
    )

    result = await query(filters, pagination)

    assert result is expected
    metadata_reader.list_by_filter.assert_called_once_with(filters, pagination)
    identity_provider.get_current_user_id.assert_called_once()
