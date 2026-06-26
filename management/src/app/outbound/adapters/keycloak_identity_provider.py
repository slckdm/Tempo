from fastapi import Request
from jwt.exceptions import ExpiredSignatureError
from toolkit.clients import KeycloakClient
from toolkit.entities import ServiceAccount
from toolkit.security.utils import decode_token, normalize_public_key
from toolkit.service.exceptions import Forbidden, Unauthorized
from toolkit.types_ import UserID

from app.core.common.ports.cacher import Cacher
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.security.oauth2_scheme import oauth2_scheme


class KeycloakIdentityProvider(IdentityProvider):
    def __init__(self, client: KeycloakClient, request: Request, cacher: Cacher) -> None:
        self._token = oauth2_scheme(request)
        self._client = client
        self._cacher = cacher

    async def get_current_user_id(self) -> UserID:
        token = await self._token
        jwk: str | None = await self._cacher.get("service_keycloak_jwk")

        if not jwk:
            jwk = await self._client.get_jwk()
            await self._cacher.set("service_keycloak_jwk", jwk)

        if not token:
            raise Unauthorized

        try:
            user_data = decode_token(token, normalize_public_key(jwk))
        except ExpiredSignatureError as expired_token_exc:
            raise Unauthorized from expired_token_exc
        if isinstance(user_data, ServiceAccount):
            raise Forbidden

        return UserID(user_data.id)
