import logging
from functools import lru_cache
from importlib.metadata import distribution

from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """App settings"""

    class ConfigDict:
        env_file = ".env"

    APP_VERSION: str
    APP_MODE: str
    APP_CONTAINERIZED: str
    APP_ENABLE_DOCS: bool = True

    APP_LOG_LEVEL: str
    APP_LOG_PATH: str | None = None

    APP_TOKEN: str

    DEFAULT_API_RETRY_COUNT: int = 5
    DEFAULT_API_RETRY_START_TIMEOUT: float = 1
    VERIFY_SSL: bool = True

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TIMEOUT: int = 60
    POSTGRES_MIN_CONNECTIONS: int = 2
    POSTGRES_MAX_CONNECTIONS: int = 10

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_LIFETIME_MINUTES: int = 5


@lru_cache()
def get_settings() -> Settings:
    return Settings(  # type: ignore
        APP_VERSION=distribution("todo-api").version,
    )
