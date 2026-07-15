"""Keycloak application adapters."""

from uuid import UUID

from jwt.exceptions import PyJWTError

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    IdentityProvider,
    ServiceAccount,
    TokenProvider,
    User,
)
from tempo_toolkit.application.cache import Cache
from tempo_toolkit.application.errors import Forbidden, Unauthorized
from tempo_toolkit.contracts.identifiers import UserID

from .client import KeycloakClient
from .jwt import decode_token, get_user_data_from_token, normalize_public_key


class KeycloakIdentityProvider(IdentityProvider):
    """Resolve the current user from a Keycloak token."""

    def __init__(
        self, client: KeycloakClient, token_provider: TokenProvider, cache: Cache
    ) -> None:
        """Initialize the adapter with Keycloak and request ports."""
        self._token_provider = token_provider
        self._client = client
        self._cache = cache

    async def get_current_user_id(self, audience: list[str]) -> UserID:
        """Return the verified current user identifier."""
        token = await self._token_provider.get_token()
        if not token:
            raise Unauthorized

        jwk: str | None = await self._cache.get("service_keycloak_jwk")
        if not jwk:
            jwk = await self._client.get_jwk()
            await self._cache.set("service_keycloak_jwk", jwk)

        try:
            user_data = get_user_data_from_token(
                decode_token(token, normalize_public_key(jwk), audience)
            )
        except PyJWTError as invalid_token_exception:
            raise Unauthorized from invalid_token_exception
        return UserID(user_data.id)


class KeycloakAuthorizedUserFinder(AuthorizedUserFinder):
    """Find authorized users through the Keycloak administrative API."""

    def __init__(self, client: KeycloakClient) -> None:
        """Initialize the finder with a Keycloak client."""
        self._client = client

    async def get_by_id(self, user_id: UserID) -> User | ServiceAccount | None:
        """Return the authorized user, if present."""
        user = await self._client.get_user_by_id(str(user_id))
        if not user:
            return None
        return User(
            id=UserID(UUID(user["id"])),
            username=user["username"],
            email=user["email"],
            first_name=user["firstName"],
            last_name=user["lastName"],
        )
