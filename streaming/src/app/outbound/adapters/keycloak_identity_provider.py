from jwt.exceptions import PyJWTError

from toolkit.clients import KeycloakClient
from toolkit.entities import ServiceAccount
from toolkit.security.utils import decode_token, get_user_data_from_token, normalize_public_key
from toolkit.service.exceptions import Forbidden, Unauthorized
from toolkit.types_ import UserID

from app.core.common.auth.service import AuthorizationService
from app.core.common.ports.identity_provider import IdentityProvider


class KeycloakIdentityProvider(IdentityProvider):
    def __init__(self, client: KeycloakClient, auth_service: AuthorizationService) -> None:
        self._auth_service = auth_service
        self._client = client

    async def get_current_user_id(self, audience: list[str]) -> UserID:
        jwk = await self._client.get_jwk()
        token = await self._auth_service.get_token()
        if not token:
            raise Unauthorized
        try:
            user_data = get_user_data_from_token(
                decode_token(token, normalize_public_key(jwk), audience)
            )
        except PyJWTError as expired_token_exc:
            raise Unauthorized from expired_token_exc
        if isinstance(user_data, ServiceAccount):
            raise Forbidden

        return UserID(user_data.id)
