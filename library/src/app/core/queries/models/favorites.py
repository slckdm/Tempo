from pydantic import BaseModel

from app.core.queries.models.favorite import FavoriteQM


class FavoritesQM(BaseModel):
    favorites: list[FavoriteQM]
