
from fastapi import Request
from fastapi.security import OAuth2
from toolkit.values import Token


class AuthorizationService:

    def __init__(self, request: Request, schemas: list[OAuth2]) -> None:
        self.__request = request
        self.__schemas = schemas

    async def get_token(self) -> Token | None:
        for schema_ in self.__schemas:
            token = await schema_(self.__request)
            if token:
                return Token(token)

        return None
