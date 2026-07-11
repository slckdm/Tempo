from pydantic import BaseModel

from tempo_toolkit.contracts.uploads import UploadURN


class TracksQM(BaseModel):
    tracks: list[UploadURN]
