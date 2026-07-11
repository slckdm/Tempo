"""Shared application errors."""


class TempoBaseError(Exception):
    """Base Tempo application error."""

    message: str | None = None
    data: dict

    def __init__(self, message: str | None = None, data: dict | None = None) -> None:
        """Initialize an application error."""
        self.message = message or self.__class__.message
        self.data = data or {}
        super().__init__(message) if message else super().__init__()


class Unauthorized(TempoBaseError):
    """Authentication is required or invalid."""


class Forbidden(TempoBaseError):
    """The authenticated principal cannot perform the operation."""


class NotFound(TempoBaseError):
    """The requested resource does not exist."""


class UnsupportedMediaType(TempoBaseError):
    """The supplied media type is unsupported."""


class Conflict(TempoBaseError):
    """The requested operation conflicts with current state."""


class ResourceAlreadyExists(TempoBaseError):
    """The resource already exists."""


class ObjectStorageError(TempoBaseError):
    """Object storage operation failed."""


class OutboxStorageError(TempoBaseError):
    """Outbox persistence operation failed."""


class TransactionError(TempoBaseError):
    """Database transaction failed."""
