from toolkit.service.exceptions import TempoBaseError


class MetadataAlreadyProcessed(TempoBaseError):
    detail = "Metadata has been already processed."


class TagParseError(TempoBaseError):
    detail = "Cannot parse tags."
