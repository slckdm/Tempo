from dishka import Provider, Scope, provide

from tempo_toolkit.application.cache import Cache
from tempo_toolkit.application.persistence import Flusher, Transaction
from tempo_toolkit.application.time import UTCTimer
from tempo_toolkit.infrastructure.cache import RedisCache
from tempo_toolkit.infrastructure.database import SQLAlchemyFlusher, SQLAlchemyTransaction
from tempo_toolkit.infrastructure.time import SystemUTCTimer

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists
from app.outbound.adapters.sqla_favorite_storage import SQLAFavoriteStorage
from app.outbound.adapters.sqla_playlist_track_storage import SQLAPlaylistTrackStorage


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    cacher = provide(RedisCache, provides=Cache)

    # ports
    flusher = provide(SQLAlchemyFlusher, provides=Flusher)
    transaction = provide(SQLAlchemyTransaction, provides=Transaction)
    favorite_storage = provide(SQLAFavoriteStorage, provides=FavoriteStorage)
    playlist_track_storage = provide(SQLAPlaylistTrackStorage, provides=PlaylistTrackStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    remove_track_from_favorites = provide(RemoveTrackFromFavorites)
    remove_track_from_playlists = provide(RemoveTrackFromPlaylists)
