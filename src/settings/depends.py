from sqlalchemy.orm import sessionmaker
from src.settings.db import async_session


async def get_session() -> sessionmaker:
    async with async_session() as session:
        yield session
