from jwt import decode
from .utils import get_service_account_data_from_token, get_user_data_from_token
from .models import User, ServiceAccount
from toolkit.clients import APIClient
from .keycloak_configuration import KeycloakConfig
from http import HTTPMethod


class KeycloakClient(APIClient):

    def __init__(
        self,
        configuration: KeycloakConfig
    ) -> None:
        super().__init__(configuration.url)
        self.configuration = configuration

    async def get_jwk(self) -> str:
        url = self.configuration.url + "/realms/" + self.configuration.realm
        payload = await self.request(HTTPMethod.GET, url)
        return payload["public_key"]


    @staticmethod
    def normalize_public_key(public_key: str | None) -> str:
        if public_key is None:
            return ""
        return f"-----BEGIN PUBLIC KEY-----\n {public_key} \n-----END PUBLIC KEY-----"

    async def decode_token(self, token: str) -> User | ServiceAccount:
        validation_options = {
            "options": {
                "verify_exp": True,
                "verify_aud": False,
            },
            "audience": [],
        }
        payload = decode(
            jwt=token,
            key=self.normalize_public_key(await self.get_jwk()),
            algorithms=["RS256"],
            verify=False,
            **validation_options
        )

        if "client_id" not in payload:
            return get_user_data_from_token(payload)
        else:
            return get_service_account_data_from_token(payload)
