import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider

from app.core.queries.get_playlist_tracks import GetPlaylistTracks
from app.core.queries.ports.tracks_reader import TrackReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_playlist_id,
    create_tracks_qm,
    create_user,
)


def make_get_playlist_tracks_query(
    track_reader: TrackReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetPlaylistTracks:
    return GetPlaylistTracks(
        tracks_reader=track_reader,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
    )


@pytest.mark.asyncio
async def test_get_playlist_tracks_success(
    track_reader: TrackReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    playlist_id = create_playlist_id()
    expected = create_tracks_qm()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    track_reader.get_list.return_value = expected
    query = make_get_playlist_tracks_query(
        track_reader,
        identity_provider,
        authorized_user_finder,
    )

    result = await query(playlist_id)

    assert result is expected
    track_reader.get_list.assert_called_once_with(user.id, playlist_id)
