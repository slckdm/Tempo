from dishka import Provider, provide

from toolkit.entities import ServiceAccount, User

from app.outbound.keycloak_auth_user_finder import AuthorizedUserFinder
from app.outbound.keycloak_identity_provider import IdentityProvider


class AuthorizationError(Exception): ...


class CurrentUserService(Provider):
    def __init__(
        self, identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
    ) -> None:
        self._identity_provider = identity_provider
        self._authorized_user_finder = authorized_user_finder

    @provide
    async def get_current_user(self) -> User | ServiceAccount:
        current_user_id = await self._identity_provider.get_current_user_id()
        user = await self._authorized_user_finder.get_by_id(current_user_id)

        if not user:
            raise AuthorizationError

        return user
