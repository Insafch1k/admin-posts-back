import psycopg2
from loguru import logger
from .config import settings

def connection_db():
    dbname = settings.DB_NAME
    user = settings.DB_USER
    password = settings.DB_PASSWORD
    host = settings.DB_HOST
    port = settings.DB_PORT
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            port=port
        )
        logger.info("Successfully connected to PostgreSQL")
        return connection

    except Exception as ex:
        logger.error(f'Sorry failed to connect: {ex}')
        return None
