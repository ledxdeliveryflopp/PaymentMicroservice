from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.settings.settings import settings

engine = create_async_engine(
    url=settings.sql_settings.db_full_url,
    echo=False
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()
