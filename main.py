from application.api import app
from utils.database_manager import DatabaseManager
from utils.config import Settings

from sqlalchemy import create_engine
import domain  # Импортируем модуль, чтобы все модели зарегистрировались
from utils.connection_db import connection_db

config = Settings()
DatabaseManager.initialize(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)