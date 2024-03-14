from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class SqlSettings(BaseSettings):
    """Настройки для SQL"""

    sql_user: str
    sql_password: str
    sql_host: str
    sql_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(BaseSettings):
    sql_settings: SqlSettings


@lru_cache()
def init_settings():
    all_settings = Settings(sql_settings=SqlSettings())
    return all_settings


settings = init_settings()
