from typing import List
from loguru import logger
from .dal import ChannelDAL
from .schemas import ChannelResponse
from utils.data_state import DataState, DataSuccess, DataFailedMessage


class ChannelBL:
    def __init__(self):
        self.dal = ChannelDAL()

    def get_user_channels(self, user_id: int) -> DataState[List[ChannelResponse]]:
        """
        Получает каналы пользователя и преобразует их в ChannelResponse
        """
        try:
            db_result = self.dal.get_user_channels(user_id)

            if db_result.error_message:
                return DataFailedMessage(error_message=db_result.error_message)

            if not db_result.data:
                return DataFailedMessage(error_message="Каналы не найдены")

            channels_response = [
                ChannelResponse(
                    id=channel.channel_id,
                    name=channel.channel_username,
                    avatarUrl=channel.channel_photo or "default_avatar.jpg"
                )
                for channel in db_result.data
            ]

            return DataSuccess(data=channels_response)  # Явно указываем параметр data

        except Exception as e:
            logger.error(f"BL error: {e}")
            return DataFailedMessage(error_message="Ошибка обработки данных")