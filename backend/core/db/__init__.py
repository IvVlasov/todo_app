import asyncpg

from backend.settings import get_settings


async def create_postgres_connection_pool():
    settings = get_settings()
    return await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        command_timeout=settings.POSTGRES_TIMEOUT,
        min_size=settings.POSTGRES_MIN_CONNECTIONS,
        max_size=settings.POSTGRES_MAX_CONNECTIONS,
    )
