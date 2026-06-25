
from toolkit.entities import ServiceAccount, User
from toolkit.service.exceptions import UnauthorizedException

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider


class CurrentUserService:
    def __init__(
        self, identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
    ) -> None:
        self._identity_provider = identity_provider
        self._authorized_user_finder = authorized_user_finder

    async def get_current_user(self) -> User | ServiceAccount:
        current_user_id = await self._identity_provider.get_current_user_id()
        user = await self._authorized_user_finder.get_by_id(current_user_id)

        if not user:
            raise UnauthorizedException

        return user
