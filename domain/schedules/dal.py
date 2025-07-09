import logging
from utils import connection_db
from utils.database_manager import DatabaseManager

class ScheduleDAL:
    @staticmethod
    def get_schedules_by_channel(channel_id):
        """
        Возвращает все расписания публикаций для конкретного канала.
        """
        from utils.database_manager import DatabaseManager
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT schedule_id, channel_id, post_id, publish_time, published_at FROM schedules WHERE channel_id = %s",
                    (channel_id,)
                )
                rows = cursor.fetchall()
                return rows if rows else []
        except Exception as e:
            logging.error(f"Error fetching schedules by channel with psycopg2: {e}")
            return []

    @staticmethod
    def delete_schedules_by_channel(channel_id):
        """
        Удаляет все расписания для конкретного канала.
        """
        from utils.database_manager import DatabaseManager
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM schedules WHERE channel_id = %s",
                    (channel_id,)
                )
        except Exception as e:
            logging.error(f"Error deleting schedules by channel: {e}")
            raise

    @staticmethod
    def get_schedule_settings(channel_id):
        """
        Получает флаги расписания для канала из schedule_settings.
        """
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT duplication, dublication_week, random FROM schedule_settings WHERE channel_id = %s",
                    (channel_id,)
                )
                row = cursor.fetchone()
                if row:
                    return {
                        'duplication': row.get('duplication', False),
                        'dublicationWeek': row.get('dublication_week', False),
                        'random': row.get('random', False)
                    }
                else:
                    return {
                        'duplication': False,
                        'dublicationWeek': False,
                        'random': False
                    }
        except Exception as e:
            logging.error(f"Error fetching schedule settings: {e}")
            return {
                'duplication': False,
                'dublicationWeek': False,
                'random': False
            }

    @staticmethod
    def upsert_schedule_settings(channel_id, duplication, dublication_week, random):
        """
        Вставляет или обновляет флаги расписания для канала в schedule_settings.
        """
        from utils.database_manager import DatabaseManager
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO schedule_settings (channel_id, duplication, dublication_week, random)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (channel_id) DO UPDATE SET
                        duplication = EXCLUDED.duplication,
                        dublication_week = EXCLUDED.dublication_week,
                        random = EXCLUDED.random
                    """,
                    (channel_id, duplication, dublication_week, random)
                )
        except Exception as e:
            logging.error(f"Error upserting schedule settings: {e}")
            raise

    @staticmethod
    def insert_schedules(schedules):
        """
        Вставляет несколько расписаний в таблицу schedules.
        schedules: список словарей с ключами channel_id, post_id, publish_time
        """
        from utils.database_manager import DatabaseManager
        try:
            with DatabaseManager.get_cursor() as cursor:
                for sched in schedules:
                    cursor.execute(
                        """
                        INSERT INTO schedules (channel_id, post_id, publish_time)
                        VALUES (%s, %s, %s)
                        """,
                        (sched['channel_id'], sched['post_id'], sched['publish_time'])
                    )
        except Exception as e:
            logging.error(f"Error inserting schedules: {e}")
            raise

    @staticmethod
    def update_schedule_time(schedule_id: int, publish_time) -> bool:
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "UPDATE schedules SET publish_time = %s WHERE schedule_id = %s",
                    (publish_time, schedule_id)
                )
                updated = cursor.rowcount
                return updated > 0
        except Exception as e:
            logging.error(f"Error updating schedule time {schedule_id}: {e}")
            return False

    @staticmethod
    def create_schedule(channel_id: int, post_id: int, publish_time) -> bool:
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "INSERT INTO schedules (channel_id, post_id, publish_time) VALUES (%s, %s, %s)",
                    (channel_id, post_id, publish_time)
                )
                return True
        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            return False

    @staticmethod
    def delete_schedules_by_post_id(post_id):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM schedules WHERE post_id = %s", (post_id,)
                )
                return True
        except Exception as e:
            logging.error(f"Error deleting schedule: {e}")
            return False