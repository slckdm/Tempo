
import pytest

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from tests.unit.core.factories import create_current_user_service


@pytest.mark.asyncio
async def test_get_current_user(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder
) -> None:
    current_user_service = create_current_user_service(identity_provider, authorized_user_finder)
    await current_user_service.get_current_user()
