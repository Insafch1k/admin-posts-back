# domain/db_manager.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.config import settings

Base = declarative_base()


class DatabaseManager:
    def __init__(self):
        self._engine = None
        self._session_factory = None

    def init_db(self):
        db_url = (
            f"postgresql://{settings.USER}:{settings.PASSWORD}@"
            f"{settings.HOST_NAME}:{settings.PORT_NAME}/{settings.DB_NAME}"
        )

        self._engine = create_engine(db_url, pool_pre_ping=True)
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    def get_session(self):
        if not self._session_factory:
            self.init_db()
        return self._session_factory()


db_manager = DatabaseManager()