from application.api import app

from sqlalchemy import create_engine
# from domain.base import Base
import domain  # Импортируем модуль, чтобы все модели зарегистрировались
from utils.connection_db import connection_db

# Настройка подключения к БД
conn = connection_db()


# Создание всех таблиц (если их нет)
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)