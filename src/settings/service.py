from dataclasses import dataclass
from src.settings.repository import SessionRepository


@dataclass
class SessionService:
    _session_repository: SessionRepository

    async def save_update_object(self, save_object: dict):
        return await self._session_repository.save_update_object(save_object=save_object)

    async def delete_object(self, delete_object: dict):
        return await self._session_repository.delete_object(delete_object=delete_object)
