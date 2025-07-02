from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()


from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import Pool
from typing import Optional, Callable
from utils.config import settings


class DatabaseManager:
    def __init__(self):
        self._engine = None
        self._SessionLocal = None
        self._initialized = False

    def init_db(self) -> None:
        """Инициализирует движок и фабрику сессий"""
        if self._initialized:
            return

        try:
            connection_str = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@" \
                             f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

            # Создаем engine с настройками пула
            self._engine = create_engine(
                url=connection_str,
                pool_size=10,  # Размер основного пула
                max_overflow=5,  # Сколько можно создать сверху
                pool_recycle=1800,  # Пересоздавать соединение каждые 30 минут
                pool_pre_ping=True,  # Проверка перед использованием
                echo=False  # Не выводить SQL в логи (True для отладки)
            )

            # Проверяем подключение
            with self._engine.connect() as conn:
                logger.info("✅ Successfully connected to the database")

            # Создаем фабрику сессий
            self._SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )

            self._initialized = True

        except Exception as ex:
            logger.error(f"❌ Failed to initialize database: {ex}")
            raise

    def get_session(self) -> Optional[Callable[[], scoped_session]]:
        """Возвращает функцию, вызов которой создаёт новую scoped_session"""

        if not self._initialized or self._SessionLocal is None:
            logger.warning("⚠️ Database not initialized")
            return None

        db_session = scoped_session(self._SessionLocal)

        return db_session

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._SessionLocal


# Глобальный экземпляр менеджера БД
db_manager = DatabaseManager()


def connect_db() -> Optional[Callable[[], scoped_session]]:
    """
    Функция для использования в приложении.
    Возвращает callable, который создаёт scoped_session
    """
    db_manager.init_db()
    return db_manager.get_session()
