from src.settings.db import async_session


async def get_session() -> object:
    async with async_session() as session:
        yield session
