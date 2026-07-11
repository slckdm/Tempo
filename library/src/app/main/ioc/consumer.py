from dishka import Provider, Scope, provide

from toolkit.common.adapters.redis_cacher import RedisCacher
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.remove_track_from_favorites import RemoveTrackFromFavorites
from app.core.commands.remove_track_from_playlists import RemoveTrackFromPlaylists
from app.outbound.adapters.sqla_favorite_storage import SQLAFavoriteStorage
from app.outbound.adapters.sqla_playlist_track_storage import SQLAPlaylistTrackStorage


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
