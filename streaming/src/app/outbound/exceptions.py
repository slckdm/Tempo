from toolkit.service.exceptions import TempoBaseError


class StorageError(TempoBaseError):
    ...

class ObjectNotFound(StopAsyncIteration):
    ...
