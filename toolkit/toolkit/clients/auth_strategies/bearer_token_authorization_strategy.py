from .abstract_authorization_strategy import AbstractAuthorizationStrategy


class BearerTokenAuthorizationStrategy(AbstractAuthorizationStrategy):

    def __init__(self, token: str) -> None:
        self.token = token

    def get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}
