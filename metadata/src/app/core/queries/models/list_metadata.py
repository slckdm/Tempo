from pydantic import BaseModel

from app.core.queries.models.metadata import MetadataQM


class ListMetadataQM(BaseModel):
    metadata: list[MetadataQM]
    total: int
    limit: int
    offset: int
