from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class JwtSettings(BaseSettings):
    """Настройки для JWT токенов"""
    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SqlSettings(BaseSettings):
    """Настройки для SQL"""
    sql_user: str
    sql_password: str
    sql_host: str
    sql_port: str
    sql_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def db_full_url(self) -> str:
        return (f"postgresql+asyncpg://{self.sql_user}:{self.sql_password}@"
                f"{self.sql_host}:{self.sql_port}/{self.sql_name}")


class YookassaSettings(BaseSettings):
    """Настройки Yookassa"""
    account_id: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AlembicSettings(BaseSettings):
    """Настройки таблиц alembic"""
    alembic_exclude_tables: list = ['token', 'code']


class Settings(BaseSettings):
    jwt_settings: JwtSettings
    sql_settings: SqlSettings
    yookassa_settings: YookassaSettings
    alembic_settings: AlembicSettings


@lru_cache()
def init_settings() -> object:
    """Инициализация настроек"""
    return Settings(jwt_settings=JwtSettings(), sql_settings=SqlSettings(),
                    yookassa_settings=YookassaSettings(), alembic_settings=AlembicSettings())


settings = init_settings()
