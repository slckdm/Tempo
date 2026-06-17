from dataclasses import dataclass
from typing import Iterator



@dataclass(frozen=True)
class AudioObject:
    status_code: int
    content_type: str
    content_range: int | None
    content_length: int
    chunks: Iterator[bytes]
