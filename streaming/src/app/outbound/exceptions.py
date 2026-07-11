from toolkit.service.exceptions import TempoBaseError


class ObjectNotFound(StopAsyncIteration, TempoBaseError):
    ...


class ObjectRangeError(TempoBaseError):
    ...
