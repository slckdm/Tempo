from dataclasses import dataclass, asdict


@dataclass(frozen=True, kw_only=True)
class CollectionMetadata:
    title: str | None = None
    artist: str | None = None
    album: str | None = None
    genre: str | None = None
    year: str | None = None
    content_type: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
