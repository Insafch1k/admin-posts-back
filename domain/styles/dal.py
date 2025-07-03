from sqlalchemy.orm import Session
from utils.connection_db import connection_db
from domain.prompts import PromptSchema
from .schemas import StyleSchema
from utils.data_state import DataState, DataSuccess, DataFailedMessage
from loguru import logger


class StyleDAL:
    @classmethod
    def get_channel_styles(cls, channel_id: int) -> DataState:
        """Получить стили и промты для канала"""
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка подключения к базе данных')

        session = Session()
        try:
            # Альтернативный запрос без сложных join
            styles = session.query(Style). \
                join(Prompt, Style.style_id == Prompt.style_id). \
                filter(Prompt.channel_id == channel_id). \
                distinct().all()

            if not styles:
                return DataFailedMessage(error_message="Стили не найдены")

            result = []
            for style in styles:
                # Получаем промты для каждого стиля
                prompts = session.query(Prompt). \
                    filter(
                    Prompt.style_id == style.style_id,
                    Prompt.channel_id == channel_id
                ).all()

                result.append({
                    "style": StyleSchema.model_validate(style),  # Новый метод в Pydantic 2+
                    "prompts": [PromptSchema.model_validate(p) for p in prompts]
                })

            return DataSuccess(data=result)

        except Exception as e:
            logger.error(f"DAL error: {e}")
            return DataFailedMessage(error_message='Ошибка получения стилей')
        finally:
            session.close()