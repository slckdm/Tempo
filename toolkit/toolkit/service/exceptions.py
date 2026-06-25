from http import HTTPStatus


class TempoBaseException(Exception):
    message: str | None = None

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.__class__.message
        super().__init__(message) if message else super().__init__()


class TempoHTTPException(TempoBaseException):
    status_code: HTTPStatus | int
    data: dict

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        super().__init__(message=message)
        self.data = data or {}


class UnauthorizedException(TempoBaseException):
    ...


class ForbiddenException(TempoBaseException):
    ...


class NotFoundException(TempoBaseException):
    ...
