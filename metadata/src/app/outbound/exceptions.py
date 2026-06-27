from toolkit.service.exceptions import TempoBaseError


class ObjectStorageError(TempoBaseError):
    ...


class MetadataReaderError(TempoBaseError):
    ...


class MetadataStorageError(TempoBaseError):
    ...


class MetadataParserError(TempoBaseError):
    ...


class OutboxStorageError(TempoBaseError):
    ...


class TransactionError(TempoBaseError):
    ...


class FlusherError(TempoBaseError):
    ...
