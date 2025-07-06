import logging
from utils.connection_db import connection_db

class ScheduleDAL:
    @staticmethod
    def get_schedules_by_channel(channel_id):
        """
        Возвращает все расписания публикаций для конкретного канала.
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute("SELECT schedule_id, channel_id, post_id, publish_time, published_at FROM schedules WHERE channel_id = %s", (channel_id,))
            rows = cur.fetchall()
            schedules = [
                {
                    "schedule_id": row[0],
                    "channel_id": row[1],
                    "post_id": row[2],
                    "publish_time": row[3],
                    "published_at": row[4]
                }
                for row in rows
            ]
            cur.close()
            return schedules
        except Exception as e:
            logging.error(f"Error fetching schedules by channel with psycopg2: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_schedules_by_channel(channel_id):
        """
        Удаляет все расписания для конкретного канала.
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM schedules WHERE channel_id = %s", (channel_id,))
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error deleting schedules by channel: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_schedule_settings(channel_id):
        """
        Получает флаги расписания для канала из schedule_settings.
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute("SELECT duplication, dublication_week, random FROM schedule_settings WHERE channel_id = %s", (channel_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return {
                    'duplication': row[0],
                    'dublicationWeek': row[1],
                    'random': row[2]
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
        finally:
            if conn:
                conn.close()

    @staticmethod
    def upsert_schedule_settings(channel_id, duplication, dublication_week, random):
        """
        Вставляет или обновляет флаги расписания для канала в schedule_settings.
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute(
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
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error upserting schedule settings: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()

    @staticmethod
    def insert_schedules(schedules):
        """
        Вставляет несколько расписаний в таблицу schedules.
        schedules: список словарей с ключами channel_id, post_id, publish_time
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            for sched in schedules:
                cur.execute(
                    """
                    INSERT INTO schedules (channel_id, post_id, publish_time)
                    VALUES (%s, %s, %s)
                    """,
                    (sched['channel_id'], sched['post_id'], sched['publish_time'])
                )
            conn.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error inserting schedules: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()