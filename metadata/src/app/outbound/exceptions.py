from toolkit.service.exceptions import TempoBaseException


class ObjectStorageError(TempoBaseException):
    ...


class MetadataReaderError(TempoBaseException):
    ...


class MetadataStorageError(TempoBaseException):
    ...


class MetadataParserError(TempoBaseException):
    ...


class OutboxStorageError(TempoBaseException):
    ...


class TransactionError(TempoBaseException):
    ...


class FlusherError(TempoBaseException):
    ...
