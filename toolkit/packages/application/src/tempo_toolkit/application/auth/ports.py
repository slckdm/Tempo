"""Authentication ports."""

from typing import Protocol

from tempo_toolkit.contracts.identifiers import UserID

from .models import ServiceAccount, User
from .types import Token


class TokenProvider(Protocol):
    """Provide an authentication token for the current request."""

    async def get_token(self) -> Token | None:
        """Return the current request token, if present."""
        ...


class IdentityProvider(Protocol):
    """Resolve the current principal identifier."""

    async def get_current_user_id(self, audience: list[str]) -> UserID:
        """Return the current user identifier."""
        ...


class AuthorizedUserFinder(Protocol):
    """Find an authorized principal."""

    async def get_by_id(self, user_id: UserID) -> User | ServiceAccount | None:
        """Find an authorized principal by identifier."""
        ...
