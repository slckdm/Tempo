from http import HTTPStatus

from toolkit.service.exceptions import TempoBaseException


class BaseError(TempoBaseException):
    default_message: str | None = None

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class MetadataAlreadyProcessed(TempoBaseException):
    status_code = HTTPStatus.FORBIDDEN
    detail = "Metadata has been already processed."


class TagParseError(TempoBaseException):
    status_code = 500
    detail = "Cannot parse tags."
