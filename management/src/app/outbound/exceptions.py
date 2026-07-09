from toolkit.service.exceptions import TempoBaseError


class ObjectStorageError(TempoBaseError):
    ...


class OutboxStorageError(TempoBaseError):
    ...


class TransactionError(TempoBaseError):
    ...


class FlusherError(TempoBaseError):
    ...
