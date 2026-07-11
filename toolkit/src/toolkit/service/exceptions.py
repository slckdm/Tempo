from http import HTTPStatus


class TempoBaseError(Exception):
    message: str | None = None
    data: dict

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        self.message = message or self.__class__.message
        self.data = data or {}
        super().__init__(message) if message else super().__init__()


class TempoHTTPError(TempoBaseError):
    status_code: HTTPStatus | int

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        super().__init__(message=message, data=data)


class Unauthorized(TempoBaseError):
    ...


class Forbidden(TempoBaseError):
    ...


class NotFound(TempoBaseError):
    ...


class UnsupportedMediaType(TempoBaseError):
    ...


class Conflict(TempoBaseError):
    ...


class ResourceAlreadyExists(TempoBaseError):
    ...


class ObjectStorageError(TempoBaseError):
    ...


class OutboxStorageError(TempoBaseError):
    ...


class TransactionError(TempoBaseError):
    ...


class FlusherError(TempoBaseError):
    ...
