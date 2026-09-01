from uuid import uuid4

import pytest

from tempo_toolkit.application.auth import AuthorizedUserFinder, IdentityProvider

from app.core.common.enums.collections import Collections
from app.core.queries.get_similar_tracks import GetSimilarTracks
from app.core.queries.ports.feature_reader import FeatureReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_similarity,
    create_user,
)


def make_query(
    feature_reader: FeatureReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetSimilarTracks:
    return GetSimilarTracks(
        feature_reader=feature_reader,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
    )


@pytest.mark.asyncio
async def test_get_similar_tracks_success(
    feature_reader: FeatureReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    upload_id = uuid4()
    expected = [create_similarity(), create_similarity(score=0.8)]
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    feature_reader.get_similar.return_value = expected
    query = make_query(feature_reader, identity_provider, authorized_user_finder)

    result = await query(upload_id)

    assert result.similar_tracks == expected
    identity_provider.get_current_user_id.assert_awaited_once_with(["tempo:etc"])
    authorized_user_finder.get_by_id.assert_awaited_once_with(user.id)
    feature_reader.get_similar.assert_awaited_once_with(
        Collections.TRACK_FEATURES,
        id=upload_id,
    )
