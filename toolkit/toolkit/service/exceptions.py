from http import HTTPStatus


class TempoBaseException(Exception):
    message: str | None = None
    data: dict

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        self.message = message or self.__class__.message
        self.data = data or {}
        super().__init__(message) if message else super().__init__()


class TempoHTTPException(TempoBaseException):
    status_code: HTTPStatus | int

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        super().__init__(message=message, data=data)


class UnauthorizedException(TempoBaseException):
    ...


class ForbiddenException(TempoBaseException):
    ...


class NotFoundException(TempoBaseException):
    ...
