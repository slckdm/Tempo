import pytest

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.identity_provider import IdentityProvider

from app.core.queries.get_favorites import GetFavorites
from app.core.queries.ports.favorite_reader import FavoriteReader
from tests.unit.core.factories import (
    create_current_user_service,
    create_favorites_qm,
    create_user,
)


def make_get_favorites_query(
    favorite_reader: FavoriteReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> GetFavorites:
    return GetFavorites(
        favorite_reader=favorite_reader,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
    )


@pytest.mark.asyncio
async def test_get_favorites_success(
    favorite_reader: FavoriteReader,
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    expected = create_favorites_qm()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_reader.get_list.return_value = expected
    query = make_get_favorites_query(
        favorite_reader,
        identity_provider,
        authorized_user_finder,
    )

    result = await query()

    assert result is expected
    favorite_reader.get_list.assert_called_once_with(user.id)
    identity_provider.get_current_user_id.assert_called_once_with(["tempo:etc"])
