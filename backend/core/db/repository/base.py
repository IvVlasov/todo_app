from fastapi import FastAPI

from backend.core.db.postgres import PostgresConnectorInterface, get_postgres_connector


class BaseRepository:
    """Base repository"""

    def __init__(self, app: FastAPI):
        self.connector: PostgresConnectorInterface = get_postgres_connector(app)
