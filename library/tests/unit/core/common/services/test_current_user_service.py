import pytest

from toolkit.service.exceptions import Unauthorized

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from tests.unit.core.factories import create_current_user_service, create_user


@pytest.mark.asyncio
async def test_get_current_user_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    current_user_service = create_current_user_service(
        identity_provider,
        authorized_user_finder,
    )

    result = await current_user_service.get_current_user(["tempo:etc"])

    assert result is user
    identity_provider.get_current_user_id.assert_called_once_with(["tempo:etc"])
    authorized_user_finder.get_by_id.assert_called_once_with(user.id)


@pytest.mark.asyncio
async def test_get_current_user_unauthorized(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> None:
    user = create_user()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = None
    current_user_service = create_current_user_service(
        identity_provider,
        authorized_user_finder,
    )

    with pytest.raises(Unauthorized):
        await current_user_service.get_current_user(["tempo:etc"])
