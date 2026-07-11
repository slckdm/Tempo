import pytest

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.service.exceptions import NotFound

from app.core.queries.get_playlist import GetPlaylist
from app.core.queries.ports.playlist_reader import PlaylistReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist_id,
    create_playlist_qm,
    create_user,
)


def make_get_playlist_query(
    playlist_reader: PlaylistReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetPlaylist:
    return GetPlaylist(
        playlist_reader=playlist_reader,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
    )


@pytest.mark.asyncio
async def test_get_playlist_success(
    playlist_reader: PlaylistReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    playlist_id = create_playlist_id()
    expected = create_playlist_qm(id=playlist_id, user_id=user.id)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_reader.get_by_id.return_value = expected
    query = make_get_playlist_query(
        playlist_reader,
        identity_provider,
        authorized_user_finder,
    )

    result = await query(playlist_id)

    assert result is expected
    playlist_reader.get_by_id.assert_called_once_with(user.id, playlist_id)


@pytest.mark.asyncio
async def test_get_playlist_not_found(
    playlist_reader: PlaylistReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    playlist_id = create_playlist_id()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    playlist_reader.get_by_id.return_value = None
    query = make_get_playlist_query(
        playlist_reader,
        identity_provider,
        authorized_user_finder,
    )

    with pytest.raises(NotFound):
        await query(playlist_id)
