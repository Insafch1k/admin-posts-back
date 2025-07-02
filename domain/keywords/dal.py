# domain/keywords/dal.py
from sqlalchemy.orm import Session
from typing import List
from loguru import logger
from utils.connection_db import connection_db
from .base_model import Keyword
from .schemas import KeywordSchema
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from utils.connection_db import connection_db


class KeywordDAL:
    @classmethod
    def get_channel_keywords(cls, channel_id: int) -> DataState[List[KeywordSchema]]:
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка подключения к базе данных')

        session = Session()
        try:
            keywords = session.query(Keyword).filter(
                Keyword.channel_id == channel_id
            ).order_by(Keyword.keywords_id).all()

            if not keywords:
                return DataFailedMessage(error_message="Ключевые слова не найдены")

            return DataSuccess(data=[KeywordSchema.model_validate(kw) for kw in keywords])

        except Exception as e:
            logger.error(f"DAL error: {e}")
            return DataFailedMessage(error_message='Ошибка получения ключевых слов')
        finally:
            session.close()