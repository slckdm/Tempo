class BaseError(Exception):
    default_message: str | None = None

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class Unauthorized(BaseError):
    ...


class Forbidden(BaseError):
    ...
