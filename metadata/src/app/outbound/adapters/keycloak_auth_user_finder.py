from toolkit.clients import KeycloakClient
from toolkit.entities import User
from toolkit.types_ import UserID

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder


class KeycloakAuthorizedUserFinder(AuthorizedUserFinder):

    def __init__(self, client: KeycloakClient) -> None:
        self._client = client

    async def get_by_id(self, id: UserID) -> User | None:
        user_data = await self._client.get_user_by_id(str(id))

        if not user_data:
            return None

        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data["firstName"],
            last_name=user_data["lastName"],
        )
