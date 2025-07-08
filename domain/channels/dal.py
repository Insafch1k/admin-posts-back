from loguru import logger
from typing import List, Dict

from utils.connection_db import connection_db
from utils.data_state import DataState, DataSuccess, DataFailedMessage


class ChannelDAL:
    def get_user_channels(self, user_id: int) -> DataState:
        """Получить все каналы пользователя через psycopg2"""
        conn = None
        try:
            conn = connection_db()
            if not conn:
                return DataFailedMessage(error_message='Ошибка подключения к базе данных')

            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        channel_id, 
                        channel_username, 
                        channel_photo 
                    FROM channels 
                    WHERE user_id = %s
                """, (user_id,))

                channels = cursor.fetchall()

                if not channels:
                    return DataFailedMessage(error_message="Каналы не найдены")

                # Преобразуем в список словарей
                result = [
                    {
                        "channel_id": row[0],
                        "channel_username": row[1],
                        "channel_photo": row[2]
                    }
                    for row in channels
                ]
                return DataSuccess(data=result)

        except Exception as e:
            logger.error(f"DAL error: {e}")
            return DataFailedMessage(error_message='Ошибка при выполнении запроса')
        finally:
            if conn:
                conn.close()