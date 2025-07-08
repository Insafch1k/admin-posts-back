from typing import Iterator, Optional, Union, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2 import pool
from contextlib import contextmanager
import logging
from utils.config import Settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    _pool = None

    @classmethod
    def initialize(cls, config: Settings):
        """Инициализация пула соединений при старте приложения"""
        if cls._pool is None:
            try:
                cls._pool = pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    host=config.DB_HOST,
                    port=config.DB_PORT,
                    database=config.DB_NAME
                )
                logger.info("Database connection pool initialized")
            except Exception as e:
                logger.error(f"Connection pool initialization failed: {e}")
                raise

    @classmethod
    @contextmanager
    def get_cursor(cls) -> Iterator[RealDictCursor]:
        """Контекстный менеджер для безопасной работы с курсором"""
        conn = None
        try:
            conn = cls._pool.getconn()
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
            conn.commit()
        except psycopg2.Error as e:
            logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        """Закрыть все соединения при завершении приложения"""
        if cls._pool:
            cls._pool.closeall()
            logger.info("All database connections closed")


class Executor:
    @staticmethod
    @contextmanager
    def _get_cursor() -> Iterator[RealDictCursor]:
        """Контекстный менеджер для получения курсора из пула соединений"""
        with DatabaseManager.get_cursor() as cursor:
            yield cursor

    @staticmethod
    def _execute_query(
        query: str,
        params: Optional[Union[tuple, list, dict]] = None,
        fetchall: bool = False,
        fetchone: bool = False
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """Метод для выполнения SQL запросов с использованием пула соединений"""
        try:
            with Executor._get_cursor() as cursor:
                if params and isinstance(params, list):
                    cursor.executemany(query, params)
                else:
                    if params and not isinstance(params, tuple):
                        params = (params,)
                    cursor.execute(query, params or ())

                result = None
                if fetchall:
                    rows = cursor.fetchall()
                    result = [dict(row) for row in rows] if rows else None
                elif fetchone:
                    row = cursor.fetchone()
                    result = dict(row) if row else None
                return result

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise RuntimeError(f"Database operation failed: {e}")