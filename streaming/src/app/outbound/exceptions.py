from tempo_toolkit.application.errors import TempoBaseError


class ObjectNotFound(StopAsyncIteration, TempoBaseError):
    ...


class ObjectRangeError(TempoBaseError):
    ...
