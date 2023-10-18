from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    db_url: str = 'postgresql+asyncpg://user:pass@localhost/app'


@lru_cache()
def get_settings():
    return Settings()
