from uuid import uuid4

import pytest

from toolkit.common.ports.auth_user_finder import AuthorizedUserFinder
from toolkit.common.ports.flusher import Flusher
from toolkit.common.ports.identity_provider import IdentityProvider
from toolkit.common.ports.transaction import Transaction
from toolkit.common.services.current_user_service import CurrentUserService
from toolkit.service.exceptions import Forbidden, NotFound

from app.core.commands.ports.favorite_storage import FavoriteStorage
from app.core.commands.remove_favorite import RemoveFavorite
from tests.unit.core.factories import (
    create_current_user_service,
    create_favorite,
    create_user,
)


def make_remove_favorite_command(
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
    current_user_service: CurrentUserService,
) -> RemoveFavorite:
    return RemoveFavorite(
        favorite_storage=favorite_storage,
        flusher=flusher,
        transaction=transaction,
        current_user_service=current_user_service,
    )


@pytest.mark.asyncio
async def test_remove_favorite_success(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    favorite = create_favorite(user_id=user.id)
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_storage.get.return_value = favorite
    command = make_remove_favorite_command(
        favorite_storage=favorite_storage,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        flusher=flusher,
        transaction=transaction,
    )

    await command(favorite.id)

    favorite_storage.get.assert_called_once_with(favorite.id)
    favorite_storage.remove.assert_called_once_with(favorite)
    flusher.flush.assert_called_once()
    transaction.commit.assert_called_once()


@pytest.mark.asyncio
async def test_remove_favorite_not_found(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    favorite_id = uuid4()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_storage.get.return_value = None
    command = make_remove_favorite_command(
        favorite_storage=favorite_storage,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        flusher=flusher,
        transaction=transaction,
    )

    with pytest.raises(NotFound):
        await command(favorite_id)

    favorite_storage.remove.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()


@pytest.mark.asyncio
async def test_remove_favorite_forbidden(
    identity_provider: IdentityProvider,
    authorized_user_finder: AuthorizedUserFinder,
    favorite_storage: FavoriteStorage,
    flusher: Flusher,
    transaction: Transaction,
) -> None:
    user = create_user()
    favorite = create_favorite()
    identity_provider.get_current_user_id.return_value = user.id
    authorized_user_finder.get_by_id.return_value = user
    favorite_storage.get.return_value = favorite
    command = make_remove_favorite_command(
        favorite_storage=favorite_storage,
        current_user_service=create_current_user_service(
            identity_provider,
            authorized_user_finder,
        ),
        flusher=flusher,
        transaction=transaction,
    )

    with pytest.raises(Forbidden):
        await command(favorite.id)

    favorite_storage.remove.assert_not_called()
    flusher.flush.assert_not_called()
    transaction.commit.assert_not_called()
