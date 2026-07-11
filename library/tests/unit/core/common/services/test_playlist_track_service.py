from app.core.common.factories.id_factory import generate_playlist_id
from tests.unit.core.factories import create_playlist_track_service, create_upload_urn


def test_create_track() -> None:
    track_id = create_upload_urn()
    playlist_id = generate_playlist_id()
    playlist_track_service = create_playlist_track_service()

    playlist_track = playlist_track_service.create_track(
        playlist_id=playlist_id, track_id=str(track_id)
    )

    assert playlist_track.track_id == str(track_id)
