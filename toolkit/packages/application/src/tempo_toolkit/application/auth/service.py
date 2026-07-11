"""Current-user service."""

from typing import Sequence

from tempo_toolkit.application.auth.models import Account, User
from tempo_toolkit.application.errors import Forbidden, Unauthorized

from .ports import AuthorizedUserFinder, IdentityProvider


class CurrentUserService:
    """Resolve the authenticated application principal."""

    def __init__(
        self, identity_provider: IdentityProvider, authorized_user_finder: AuthorizedUserFinder
    ) -> None:
        """Initialize the service with identity ports."""
        self._identity_provider = identity_provider
        self._authorized_user_finder = authorized_user_finder

    async def get_current_user[AllowedAccount: Account](
        self, audience: list[str], account_type: Sequence[type[AllowedAccount]] = (User,)
    ) -> AllowedAccount:
        """Return the authorized current principal."""
        current_user_id = await self._identity_provider.get_current_user_id(audience)
        user = await self._authorized_user_finder.get_by_id(current_user_id)

        if not user:
            raise Unauthorized
        if type(user) not in account_type:
            raise Forbidden

        return user
