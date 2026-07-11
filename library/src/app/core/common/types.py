from typing import NewType
from uuid import UUID

PlaylistID = NewType("PlaylistID", UUID)
TrackID = NewType("TrackID", UUID)
FavoriteID = NewType("FavoriteID", UUID)
