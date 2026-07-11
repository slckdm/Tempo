from dishka import Provider, Scope, provide

from toolkit.common.adapters.keycloak_auth_user_finder import KeycloakAuthorizedUserFinder
from toolkit.common.adapters.keycloak_identity_provider import KeycloakIdentityProvider
from toolkit.common.adapters.redis_cacher import RedisCacher
from toolkit.common.adapters.sqla_flusher import SQLAFlusher
from toolkit.common.adapters.sqla_transaction import SQLATransaction
from toolkit.common.adapters.system_utc_timer import SystemUTCTimer
from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.cacher import Cacher
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.transaction import Transaction
from toolkit.common.ports.utc_timer import UTCTimer
from toolkit.common.services.current_user_service import CurrentUserService

from app.core.commands.add_favorite import AddFavorite
from app.core.commands.add_track_to_playlist import AddTrackToPlaylist
from app.core.commands.create_playlist import CreatePlaylist
from app.core.commands.delete_playlist import DeletePlaylist
from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.ports.playlist_storage import PlaylistStorage
from app.core.commands.ports.playlist_track_storage import PlaylistTrackStorage
from app.core.commands.remove_favorite import RemoveFavorite
from app.core.commands.remove_track_from_playlist import RemoveTrackFromPlaylist
from app.core.common.services.favorite_service import FavoriteService
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.services.playlist_track_service import PlaylistTrackService
from app.core.queries.get_favorites import GetFavorites
from app.core.queries.get_playlist import GetPlaylist
from app.core.queries.get_playlist_tracks import GetPlaylistTracks
from app.core.queries.get_playlists import GetPlaylists
from app.core.queries.ports.favorite_reader import FavoriteReader
from app.core.queries.ports.playlist_reader import PlaylistReader
from app.core.queries.ports.tracks_reader import TrackReader
from app.outbound.adapters.sqla_favorite_reader import SQLAFavoriteReader
from app.outbound.adapters.sqla_favorite_storage import SQLAFavoriteStorage
from app.outbound.adapters.sqla_playlist_reader import SQLAPlaylistReader
from app.outbound.adapters.sqla_playlist_storage import SQLAPlaylistStorage
from app.outbound.adapters.sqla_playlist_track_storage import SQLAPlaylistTrackStorage
from app.outbound.adapters.sqla_tracks_reader import SQLATrackReader


class CoreProvider(Provider):
    scope = Scope.REQUEST

    # common ports
    identity_provider = provide(KeycloakIdentityProvider, provides=IdentityProvider)
    authorized_user_finder = provide(KeycloakAuthorizedUserFinder, provides=AuthorizedUserFinder)
    cacher = provide(RedisCacher, provides=Cacher)

    # Services
    current_user_service = provide(CurrentUserService)
    favorite_service = provide(FavoriteService)
    playlist_service = provide(PlaylistService)
    playlist_track_service = provide(PlaylistTrackService)

    # ports
    flusher = provide(SQLAFlusher, provides=Flusher)
    transaction = provide(SQLATransaction, provides=Transaction)
    favorite_storage = provide(SQLAFavoriteStorage, provides=FavoriteStorage)
    playlist_track_storage = provide(SQLAPlaylistTrackStorage, provides=PlaylistTrackStorage)
    playlist_storage = provide(SQLAPlaylistStorage, provides=PlaylistStorage)
    utc_timer = provide(SystemUTCTimer, provides=UTCTimer)
    favorite_reader = provide(SQLAFavoriteReader, provides=FavoriteReader)
    playlist_reader = provide(SQLAPlaylistReader, provides=PlaylistReader)
    track_reader = provide(SQLATrackReader, provides=TrackReader)

    # commands
    add_favorite = provide(AddFavorite)
    add_track_to_playlist = provide(AddTrackToPlaylist)
    create_playlist = provide(CreatePlaylist)
    delete_playlist = provide(DeletePlaylist)
    remove_favorite = provide(RemoveFavorite)
    remove_track_from_playlist = provide(RemoveTrackFromPlaylist)

    # queries
    get_favorites = provide(GetFavorites)
    get_playlist = provide(GetPlaylist)
    get_playlists = provide(GetPlaylists)
    get_playlist_tracks = provide(GetPlaylistTracks)
