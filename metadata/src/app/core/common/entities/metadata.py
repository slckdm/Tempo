from dataclasses import dataclass


@dataclass(frozen=True)
class Metadata:
    duration: float | None = None
    album: str | None = None
    albumartist: str | None = None
    artist: str | None = None
    bitrate: float | None = None
    channels: int | None = None
    comment: str | None = None
    composer: str | None = None
    disc: int | None = None
    disc_total: int | None = None
    genre: str | None = None
    cover: Cover | None = None
    samplerate: int | None = None
    title: str | None = None
    track: int | None = None
    track_total: int | None = None
    year: str | None = None


@dataclass
class Cover:

    data: bytes
    mime_type: str | None
