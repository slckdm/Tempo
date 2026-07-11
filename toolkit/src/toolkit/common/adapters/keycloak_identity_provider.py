from jwt.exceptions import PyJWTError

from toolkit.clients import KeycloakClient
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.services.authorization_service import AuthorizationService
from toolkit.entities import ServiceAccount
from toolkit.security.utils import decode_token, get_user_data_from_token, normalize_public_key
from toolkit.service.exceptions import Forbidden, Unauthorized
from toolkit.types_ import UserID


class KeycloakIdentityProvider(IdentityProvider):
    def __init__(
        self, client: KeycloakClient, auth_service: AuthorizationService, cacher: Cacher
    ) -> None:
        self._auth_service = auth_service
        self._client = client
        self._cacher = cacher

    async def get_current_user_id(self, audience: list[str]) -> UserID:
        token = await self._auth_service.get_token()
        if not token:
            raise Unauthorized

        jwk: str | None = await self._cacher.get("service_keycloak_jwk")
        if not jwk:
            jwk = await self._client.get_jwk()
            await self._cacher.set("service_keycloak_jwk", jwk)

        try:
            user_data = get_user_data_from_token(
                decode_token(token, normalize_public_key(jwk), audience)
            )
        except PyJWTError as invalid_token_exc:
            raise Unauthorized from invalid_token_exc
        if isinstance(user_data, ServiceAccount):
            raise Forbidden

        return UserID(user_data.id)
