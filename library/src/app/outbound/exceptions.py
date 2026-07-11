from toolkit.service.exceptions import TempoBaseError


class FavoriteReaderError(TempoBaseError):
    ...


class FavoriteStorageError(TempoBaseError):
    ...


class PlaylistReaderError(TempoBaseError):
    ...


class PlaylistStorageError(TempoBaseError):
    ...


class TrackReaderError(TempoBaseError):
    ...


class TrackStorageError(TempoBaseError):
    ...
