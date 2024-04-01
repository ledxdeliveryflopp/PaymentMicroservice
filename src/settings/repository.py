from abc import ABC
from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository(ABC):
    session: AsyncSession

    async def session_add(self, save_object) -> object | dict:
        """Создание объекта"""
        try:
            self.session.add(instance=save_object)
            await self.session.commit()
            await self.session.refresh(instance=save_object)
            return save_object
        except IntegrityError:
            await self.session.rollback()
            return {"detail": "error."}

    async def session_delete(self, delete_object) -> dict:
        """Удаление объекта из БД"""
        try:
            await self.session.delete(instance=delete_object)
            await self.session.commit()
            return {"detail": "success deleted."}
        except IntegrityError:
            await self.session.rollback()
