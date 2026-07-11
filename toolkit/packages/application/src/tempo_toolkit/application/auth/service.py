"""Current-user service."""

from tempo_toolkit.application.errors import Unauthorized

from .models import ServiceAccount, User
from .ports import AuthorizedUserFinder, IdentityProvider


class CurrentUserService:
    """Resolve the authenticated application principal."""

    def __init__(
        self, identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
    ) -> None:
        """Initialize the service with identity ports."""
        self._identity_provider = identity_provider
        self._authorized_user_finder = authorized_user_finder

    async def get_current_user(self, audience: list[str]) -> User | ServiceAccount:
        """Return the authorized current principal."""
        current_user_id = await self._identity_provider.get_current_user_id(audience)
        user = await self._authorized_user_finder.get_by_id(current_user_id)
        if not user:
            raise Unauthorized
        return user
