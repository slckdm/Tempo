from http import HTTPStatus


class TempoException(Exception):
    status_code: HTTPStatus | int
    detail: str
    data: dict

    def __init__(self, detail: str | None = None, data: dict | None = None) -> None:
        self.detail = detail or self.__class__.detail
        self.data = data or {}


class UnauthorizedException(TempoException):
    status_code = HTTPStatus.UNAUTHORIZED
    detail = HTTPStatus.UNAUTHORIZED.phrase


class ForbiddenException(TempoException):
    status_code = HTTPStatus.FORBIDDEN
    detail = HTTPStatus.FORBIDDEN.phrase


class NotFoundException(TempoException):
    status_code = HTTPStatus.NOT_FOUND
    detail = HTTPStatus.NOT_FOUND.phrase
