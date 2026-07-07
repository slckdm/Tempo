from pydantic import BaseModel

from toolkit.types.urn import UploadURNType


class TracksQM(BaseModel):
    tracks: list[UploadURNType]
