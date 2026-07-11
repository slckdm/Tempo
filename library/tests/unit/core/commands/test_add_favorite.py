import pytest

from tempo_toolkit.application.auth import (
    AuthorizedUserFinder,
    CurrentUserService,
    IdentityProvider,
)
from tempo_toolkit.application.errors import ResourceAlreadyExists
from tempo_toolkit.application.persistence import Flusher, Transaction

from app.core.commands.add_favorite import AddFavorite, AddFavoriteRequest
from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.common.services.favorite_service import FavoriteService
from tests.unit.core.factories import (
    create_current_user_service,
    create_favorite,
    create_favorite_service,
    create_upload_urn,
    create_user,
)


def make_add_favorite_command(
    favorite_service: FavoriteService,
    flusher: Flusher,
    transaction: Transaction,
    favorite_storage: FavoriteStorage,
    current_user_service: CurrentUserService,
) -> AddFavorite:
    return AddFavorite(
        favorite_service=favorite_service,
        flusher=flusher,
        transaction=transaction,
        favorite_storage=favorite_storage,
        current_user_service=current_user_service,
    )


@pytest.mark.asyncio
async def test_add_favorite_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    track_id = create_upload_urn()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_storage.get_by_user_and_track_id.return_value = None
    command = make_add_favorite_command(
        favorite_service=create_favorite_service(),
        favorite_storage=favorite_storage,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        flusher=flusher,
        transaction=transaction,
    )

    response = await command(AddFavoriteRequest(track_id=track_id))

    assert response.track_id == track_id
    favorite_storage.get_by_user_and_track_id.assert_called_once_with(
        user_id=user.id,
        track_id=track_id,
    )
    added = favorite_storage.add.call_args.args[0]
    assert added.user_id == user.id
    assert added.track_id == str(track_id)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_add_favorite_existing_is_noop(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    track_id = create_upload_urn()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_storage.get_by_user_and_track_id.return_value = create_favorite(
        user_id=user.id,
        track_id=track_id,
    )
    command = make_add_favorite_command(
        favorite_service=create_favorite_service(),
        favorite_storage=favorite_storage,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        flusher=flusher,
        transaction=transaction,
    )

    with pytest.raises(ResourceAlreadyExists):
        await command(AddFavoriteRequest(track_id=track_id))

    favorite_storage.add.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
