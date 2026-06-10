"""Module: Bearer Token Authorization Strategy."""

from .abstract_authorization_strategy import AbstractAuthorizationStrategy


class BearerTokenAuthorizationStrategy(AbstractAuthorizationStrategy):
    """Bearer token authorization strategy."""

    def __init__(self, token: str) -> None:
        """Initialize strategy.

        Args:
            token (str): Client token.
        """
        self.token = token

    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}
