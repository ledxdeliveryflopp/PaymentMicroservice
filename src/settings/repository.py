from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    """Репозиторий для работы с БД"""
    session: AsyncSession
    object: dict

    async def save_or_update_object(self):
        """Сохранение или изменение объекта"""
        self.session.add(instance=self.object)
        await self.session.commit()
        await self.session.refresh(instance=object)

    async def delete_object(self):
        """Удаление объекта"""
        await self.session.delete(instance=object)
        await self.session.commit()
