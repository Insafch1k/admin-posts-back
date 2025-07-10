from psycopg2.extras import RealDictCursor
from sqlalchemy import select
from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage


class LastNewsDAL():
    @staticmethod
    def get_last_news_by_source_id(source_id):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = """
                    SELECT *
                    FROM lastnews
                    WHERE source_id = %(source_id)s
                    ORDER BY message_id DESC
                    LIMIT 1;
                """
                cursor.execute(sql, {'source_id': source_id})
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_last_news_by_id(last_news_id: int, updates: dict):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Построение части запроса SET col1 = %(col1)s, col2 = %(col2)s ...
                set_clause = ', '.join([f"{key} = %({key})s" for key in updates.keys()])
                query = f"""
                    UPDATE lastnews
                    SET {set_clause}
                    WHERE last_news_id = %(last_news_id)s
                    RETURNING *;
                """
                # Добавляем source_id к параметрам
                updates['last_news_id'] = last_news_id
                cursor.execute(query, updates)
                connection.commit()
                return cursor.fetchone()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def insert_last_news(updates: dict):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Получаем список колонок и соответствующих плейсхолдеров
                columns = ', '.join(updates.keys())
                placeholders = ', '.join([f"%({key})s" for key in updates.keys()])

                query = f"""
                    INSERT INTO lastnews ({columns})
                    VALUES ({placeholders})
                    RETURNING *;
                """

                cursor.execute(query, updates)
                connection.commit()
                return cursor.fetchone()

        except Exception as e:
            return {"error": str(e)}

# lsd = LastNewsDAL()
# print(lsd.get_last_news_by_source_id(1))