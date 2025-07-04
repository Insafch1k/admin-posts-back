from loguru import logger
from sqlalchemy import select, and_

from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage



class ChannelDAL:
    def get_user_channels(self, user_id: int) -> DataState:
        """Получить все каналы пользователя"""
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка в работе базы данных!')

        session = Session()
        try:
            channels = session.query(Channel).filter(Channel.user_id == user_id).all()
            return DataSuccess(data=channels)  # Явно указываем параметр data
        except Exception as e:
            logger.error(f"DAL error: {e}")
            return DataFailedMessage(error_message='Ошибка в работе базы данных!')
        finally:
            session.close()
