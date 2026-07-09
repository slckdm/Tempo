from uuid import uuid4

from faker import Faker

from toolkit.entities import User
from toolkit.types.urn import UploadURNType
from toolkit.types_ import UserID

from app.core.common.ports.auth_user_finder import AuthorizedUserFinder
from app.core.common.ports.identity_provider import IdentityProvider
from app.core.common.services.current_user_service import CurrentUserService
from app.core.common.services.favorite_service import FavoriteService
from app.core.common.services.playlist_service import PlaylistService
from app.core.common.services.playlist_track_service import PlaylistTrackService
from app.core.common.types import PlaylistID, TrackID
from app.core.models.favorite import Favorite
from app.core.models.playlist import Playlist
from app.core.models.playlist_track import PlaylistTrack
from app.core.queries.models.favorite import FavoriteQM
from app.core.queries.models.favorites import FavoritesQM
from app.core.queries.models.playlist import PlaylistQM
from app.core.queries.models.playlists import PlaylistsQM
from app.core.queries.models.tracks import TracksQM
from app.core.queries.schemas.pagination import PaginationParams

faker = Faker()


def create_current_user_service(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
) -> CurrentUserService:
    return CurrentUserService(
        identity_provider=identity_provider,
        authorized_user_finder=authorized_user_finder,
    )


def create_favorite_service() -> FavoriteService:
    return FavoriteService()


def create_playlist_service() -> PlaylistService:
    return PlaylistService()


def create_playlist_track_service() -> PlaylistTrackService:
    return PlaylistTrackService()


def create_user_id(value: UserID | None = None) -> UserID:
    return value or UserID(uuid4())


def create_user(
    id: UserID | None = None,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> User:
    return User(
        id=id or create_user_id(),
        username=username or faker.user_name(),
        first_name=first_name or faker.first_name(),
        last_name=last_name or faker.last_name(),
        email=email or faker.email(),
    )


def create_playlist_id(value: PlaylistID | None = None) -> PlaylistID:
    return value or PlaylistID(uuid4())


def create_track_id(value: TrackID | None = None) -> TrackID:
    return value or TrackID(uuid4())


def create_upload_urn(value=None) -> UploadURNType:
    return UploadURNType(value or uuid4())


def create_favorite(
    id=None,
    user_id: UserID | None = None,
    track_id: UploadURNType | None = None,
) -> Favorite:
    track_urn = track_id or create_upload_urn()
    return Favorite(
        id=id or uuid4(),
        user_id=user_id or create_user_id(),
        track_id=str(track_urn),
    )


def create_playlist(
    id: PlaylistID | None = None,
    user_id: UserID | None = None,
    name: str | None = None,
) -> Playlist:
    return Playlist(
        id=id or create_playlist_id(),
        user_id=user_id or create_user_id(),
        name=name or faker.sentence(nb_words=3),
    )


def create_playlist_track(
    id: TrackID | None = None,
    playlist_id: PlaylistID | None = None,
    track_id: UploadURNType | None = None,
) -> PlaylistTrack:
    track_urn = track_id or create_upload_urn()
    return PlaylistTrack(
        id=id or create_track_id(),
        playlist_id=playlist_id or create_playlist_id(),
        track_id=str(track_urn),
    )


def create_favorite_qm(
    id=None,
    user_id: UserID | None = None,
    track_id: UploadURNType | None = None,
) -> FavoriteQM:
    return FavoriteQM(
        id=id or uuid4(),
        user_id=user_id or create_user_id(),
        track_id=track_id or create_upload_urn(),
    )


def create_favorites_qm(favorites: list[FavoriteQM] | None = None) -> FavoritesQM:
    return FavoritesQM(favorites=favorites if favorites is not None else [create_favorite_qm()])


def create_playlist_qm(
    id: PlaylistID | None = None,
    user_id: UserID | None = None,
    name: str | None = None,
    tracks_count: int = 0,
) -> PlaylistQM:
    return PlaylistQM(
        id=id or create_playlist_id(),
        user_id=user_id or create_user_id(),
        name=name or faker.sentence(nb_words=3),
        tracks_count=tracks_count,
    )


def create_playlists_qm(
    playlists: list[PlaylistQM] | None = None,
    total: int | None = None,
    limit: int = 100,
    offset: int = 0,
) -> PlaylistsQM:
    items = playlists if playlists is not None else [create_playlist_qm()]
    return PlaylistsQM(
        playlists=items,
        total=total if total is not None else len(items),
        limit=limit,
        offset=offset,
    )


def create_tracks_qm(tracks: list[UploadURNType] | None = None) -> TracksQM:
    return TracksQM(tracks=tracks if tracks is not None else [create_upload_urn()])


def create_pagination_params(offset: int = 0, limit: int = 100) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit)
