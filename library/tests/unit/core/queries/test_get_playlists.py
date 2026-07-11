import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider

from app.core.queries.get_playlists import GetPlaylists
from app.core.queries.ports.playlist_reader import PlaylistReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_pagination_params,
    create_playlists_qm,
    create_user,
)


def make_get_playlists_query(
    playlist_reader: PlaylistReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetPlaylists:
    return GetPlaylists(
        playlist_reader=playlist_reader,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
    )


@pytest.mark.asyncio
async def test_get_playlists_success(
    playlist_reader: PlaylistReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    pagination = create_pagination_params(offset=10, limit=25)
    expected = create_playlists_qm(limit=pagination.limit, offset=pagination.offset)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_reader.get_list.return_value = expected
    query = make_get_playlists_query(
        playlist_reader,
        identity_provider,
        authorized_user_finder,
    )

    result = await query(pagination)

    assert result is expected
    playlist_reader.get_list.assert_called_once_with(user.id, pagination)
