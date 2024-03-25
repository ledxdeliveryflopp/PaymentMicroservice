from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    session: AsyncSession

    async def save_update_object(self, save_object: dict):
        try:
            self.session.add(instance=save_object)
            await self.session.commit()
            await self.session.refresh(instance=save_object)
        except IntegrityError:
            await self.session.rollback()

    async def delete_object(self, delete_object: dict):
        try:
            await self.session.delete(instance=delete_object)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
