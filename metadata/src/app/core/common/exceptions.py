from toolkit.service.exceptions import TempoBaseException


class MetadataAlreadyProcessed(TempoBaseException):
    detail = "Metadata has been already processed."


class TagParseError(TempoBaseException):
    detail = "Cannot parse tags."
