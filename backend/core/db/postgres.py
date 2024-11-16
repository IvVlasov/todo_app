import logging
from abc import ABC, abstractmethod
from typing import Any

import asyncpg
from fastapi import FastAPI

from backend.settings import get_settings


logger = logging.getLogger(__name__)


class PostgresConnectorInterface(ABC):
    """Postgres connector interface"""

    @abstractmethod
    async def connect(self) -> None:
        """Connect to Postgres"""

    @abstractmethod
    async def close(self) -> None:
        """Disconnect from postgres"""

    @abstractmethod
    async def execute_query(self, query: str, *query_params) -> None:
        """Execute query in postgres without return data

        Args:
            query (str): SQL query
        """

    @abstractmethod
    async def get_query_result_as_list(
        self, query: str, *query_params
    ) -> list[dict[str, Any]]:
        """Get sql result as list of dicts

        Args:
            query (str): SQL query

        Returns:
            list[dict[str, Any]]: Query result
        """

    @abstractmethod
    async def get_query_result_as_dict(
        self, query: str, *query_params
    ) -> dict[str, Any]:
        """Get sql result as dict (only first row)

        Args:
            query (str): SQL query

        Returns:
            dict[str, Any]: Query result
        """


class PostgresConnector(PostgresConnectorInterface):
    """Postgres connector service"""

    def __init__(self, pool: asyncpg.pool.Pool | None) -> None:
        self._pool = pool
        self.connection: asyncpg.pool.PoolConnectionProxy | None = None

    async def connect(self) -> None:
        """Connect to Postgres"""
        if self.connection:
            logger.warning("Connection already established")
            return None
        if self._pool:
            self.connection = await self._pool.acquire()
        else:
            settings = get_settings()
            self.connection = await asyncpg.connect(  # type: ignore
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                command_timeout=settings.POSTGRES_TIMEOUT,
            )

    async def close(self) -> None:
        """Disconnect from postgres"""
        if self.connection:
            if self._pool:
                await self._pool.release(self.connection)
            else:
                await self.connection.close()
            self.connection = None

    async def execute_query(self, query: str, *query_params) -> None:
        """Execute query in postgres without return data"""
        if not self.connection:
            await self.connect()
        try:
            await self.connection.execute(query, *query_params)  # type: ignore[union-attr]

        except asyncpg.exceptions.PostgresError as e:
            logger.error("Error executing query: %s", e)

        finally:
            await self.close()

    async def get_query_result_as_list(
        self, query: str, *query_params: Any
    ) -> list[dict[str, Any]]:
        """Get sql result as list of dicts"""
        if not self.connection:
            await self.connect()

        try:
            result = await self.connection.fetch(query, *query_params)  # type: ignore[union-attr]
            return [dict(row) for row in result]

        except asyncpg.exceptions.PostgresError as e:
            logger.error("Error fetching data: %s", e)
            return []

        finally:
            await self.close()

    async def get_query_result_as_dict(
        self, query: str, *query_params: Any
    ) -> dict[str, Any]:
        """Get sql result as dict (only first row)"""
        if not self.connection:
            await self.connect()

        try:
            result = await self.connection.fetchrow(query, *query_params)  # type: ignore[union-attr]
            if result:
                return dict(result)

            return {}

        except asyncpg.exceptions.PostgresError as e:
            logger.error("Error fetching data: %s", e)
            return {}

        finally:
            await self.close()


def get_postgres_connector(app: FastAPI | None = None) -> PostgresConnectorInterface:
    """Get Postgres connector"""
    if app and hasattr(app, "connection_pool"):
        return PostgresConnector(pool=app.connection_pool)  # type: ignore

    return PostgresConnector(pool=None)
