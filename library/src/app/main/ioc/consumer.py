from dishka import Provider, Scope, provide

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.flusher import Flusher
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.ports.transaction import Transaction
from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists
from app.core.common.ports.cacher import Cacher
from app.core.common.ports.utc_timer import UTCTimer
from app.outbound.adapters.redis_cacher import RedisCacher
from app.outbound.adapters.sqla_favorite_storage import SQLAFavoriteStorage
from app.outbound.adapters.sqla_flusher import SQLAFlusher
from app.outbound.adapters.sqla_playlist_track_storage import SQLAPlaylistTrackStorage
from app.outbound.adapters.sqla_transaction import SQLATransaction
from app.outbound.adapters.system_utc_timer import SystemUTCTimer


class ConsumerProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    cacher = provide(RedisCacher, provides=Cacher)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    favorite_storage = provide(SQLAFavoriteStorage, provides=FavoriteStorage)
    playlist_track_storage = provide(SQLAPlaylistTrackStorage, provides=PlaylistTrackStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)

    # commands
    remove_track_from_favorites = provide(RemoveTrackFromFavorites)
    remove_track_from_playlists = provide(RemoveTrackFromPlaylists)
