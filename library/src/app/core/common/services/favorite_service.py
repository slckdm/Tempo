from tempo_toolkit.contracts.identifiers import UserID
from tempo_toolkit.contracts.uploads import UploadURN

from app.core.common.factories.id_factory import generate_favorite_id
from app.core.models.favorite import Favorite


class FavoriteService:

    def create_favorite(self, user_id: UserID, track_id: UploadURN) -> Favorite:
        return Favorite(
            id=generate_favorite_id(),
            user_id=user_id,
            track_id=str(track_id)
        )
