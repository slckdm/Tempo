from tests.unit.core.factories import (
    create_playlist,
    create_playlist_id,
    create_playlist_service,
    create_playlist_track,
    create_user_id,
)


def test_create_playlist() -> None:
    user_id = create_user_id()
    playlist_service = create_playlist_service()

    playlist = playlist_service.create_playlist(user_id, "Daily Rotation")

    assert playlist.user_id == user_id
    assert playlist.name == "Daily Rotation"


def test_add_track_to_playlist_sets_playlist_id() -> None:
    playlist_id = create_playlist_id()
    playlist = create_playlist(id=playlist_id)
    track = create_playlist_track()
    playlist_service = create_playlist_service()

    playlist_service.add_track_to_playlist(playlist, track)

    assert track.playlist_id == playlist_id
