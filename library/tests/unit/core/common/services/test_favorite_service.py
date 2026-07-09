from tests.unit.core.factories import (
    create_favorite_service,
    create_upload_urn,
    create_user_id,
)


def test_create_favorite() -> None:
    user_id = create_user_id()
    track_id = create_upload_urn()
    favorite_service = create_favorite_service()

    favorite = favorite_service.create_favorite(user_id, track_id)

    assert favorite.user_id == user_id
    assert favorite.track_id == str(track_id)
