import logging
import os

import psycopg2
from psycopg2.extensions import connection as pg_connection
from sqlalchemy import create_engine, engine


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] - %(levelname)s - %(process)d: %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
)
logger.setLevel("DEBUG")


SCHEMA_NAME = "public"


def create_schema() -> None:
    """Create DB schema"""
    connection = get_pg_connection()

    with connection.cursor() as pg_cursor:
        pg_cursor.execute(
            f"""
            create schema if not exists {SCHEMA_NAME}
            authorization {os.getenv('POSTGRES_USER', '')}
        """
        )

    logger.info("Schema %s initialized", SCHEMA_NAME)


def get_pg_connection() -> pg_connection:
    """Get pg_connection"""
    connection = psycopg2.connect(
        user=os.getenv("POSTGRES_USER", ""),
        password=os.getenv("POSTGRES_PASSWORD", ""),
        dsn=psycopg2.extensions.make_dsn(
            host=os.getenv("POSTGRES_HOST", ""),
            port=os.getenv("POSTGRES_PORT", ""),
            dbname=os.getenv("POSTGRES_DB", ""),
        ),
    )
    connection.autocommit = True
    return connection


def get_pg_engine() -> engine.Engine:
    """Get sqlalchemy.engine.Engine"""
    url_template = "postgresql://{username}:{password}@{host}:{port}/{database}"
    pg_engine = create_engine(
        url_template.format(
            username=os.getenv("POSTGRES_USER", ""),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            host=os.getenv("POSTGRES_HOST", ""),
            port=os.getenv("POSTGRES_PORT", ""),
            database=os.getenv("POSTGRES_DB", ""),
        )
    )
    return pg_engine
