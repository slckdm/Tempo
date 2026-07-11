from abc import abstractmethod
from typing import Callable, Protocol, TypeAlias, Mapping

from toolkit.service.exceptions import Unauthorized
from toolkit.types_ import UserToken


class Request(Protocol):
    # headers: dict[str, str]
    # cookies: dict

    @property
    def headers(self) -> Mapping[str, str]: ...

    @property
    def cookies(self) -> dict[str, str]: ...


class AuthStrategy(Protocol):

    @abstractmethod
    async def __call__(self, request: Request) -> UserToken | None: ...


class BearerAuthStrategy(AuthStrategy):

    def __init__(self, auto_error: bool = True) -> None:
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> UserToken | None:
        _token = request.headers.get("Authorization")

        scheme, token = (_token or "").split(" ") or ("", "")

        if self.auto_error:
            if not _token or scheme.lower() != "bearer":
                raise Unauthorized
        else:
            return None

        return UserToken(token)


class CookieAuthStrategy(AuthStrategy):

    def __init__(self, cookie_name: str, auto_error: bool = True) -> None:
        self._cookie_name = cookie_name
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> UserToken | None:
        token = request.cookies.get(self._cookie_name)

        if self.auto_error:
            if not token:
                raise Unauthorized
        else:
            return None

        return UserToken(token)
