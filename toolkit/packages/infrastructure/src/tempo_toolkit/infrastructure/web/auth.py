"""FastAPI authentication-token integration."""

from fastapi import Request
from fastapi.security.base import SecurityBase

from tempo_toolkit.application.auth import Token, TokenProvider


class FastAPITokenProvider(TokenProvider):
    """Extract a token using configured FastAPI security schemes."""

    def __init__(self, request: Request, schemas: list[SecurityBase]) -> None:
        """Initialize the provider for the current request."""
        self.__request = request
        self.__schemas = schemas

    async def get_token(self) -> Token | None:
        """Return the first token produced by a configured schema."""
        for schema in self.__schemas:
            token = await schema(self.__request)
            if token:
                return Token(token)
        return None
