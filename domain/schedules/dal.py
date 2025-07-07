import logging

class ScheduleDAL:
    @staticmethod
    def get_schedules_by_channel(channel_id):
        """
        Возвращает все расписания публикаций для конкретного канала.
        """
        conn = None
        try:
            conn = get_db_connection()
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
