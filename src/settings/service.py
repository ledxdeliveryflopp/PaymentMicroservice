from dataclasses import dataclass
from src.settings.repository import SessionRepository


@dataclass
class SessionService(SessionRepository):
    """Сервис для взаимодействия с бд"""

    async def create_object(self, save_object: dict) -> object | dict:
        """Создать или обновить объект"""
        return await self.session_add(save_object=save_object)

    async def delete_object(self, delete_object: dict) -> dict:
        """Удалить объект"""
        return await self.session_delete(delete_object=delete_object)
