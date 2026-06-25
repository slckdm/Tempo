from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PaginationParams:
    offset: int
    limit: int
