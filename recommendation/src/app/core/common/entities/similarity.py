from dataclasses import dataclass
from uuid import UUID


@dataclass
class Similarity:
    point_id: str | int | UUID
    score: float
