from app.core.common.entities.audio_object import AudioObject
from app.core.common.types_ import UploadURNType
from app.core.ports.audio_storage import AudioStorage
from app.outbound.ports.identity_provider import IdentityProvider


class StreamAudio:

    def __init__(
        self,
        audio_storage: AudioStorage,
        identity: IdentityProvider,
    ) -> None:
        self._audio_storage = audio_storage
        self._identity = identity

    async def execute(self, id: UploadURNType, range_header: str | None) -> AudioObject:
        await self._identity.get_current_user_id()
        return await self._audio_storage.get(str(id), range_header)
