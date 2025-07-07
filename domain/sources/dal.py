from psycopg2.extras import RealDictCursor
from sqlalchemy import select, and_
from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage


class SourceDAL:
    @staticmethod
    def get_sources_by_channel_id(channel_id: int):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Получаем type_id для "Тг канал"
                sql = "SELECT type_id FROM source_type WHERE type_name = 'Тг канал'"
                cursor.execute(sql)
                data = cursor.fetchone()
                if data is None:
                    print("❌ Не найден тип 'Тг канал'")
                    return []

                id_of_news_type = data['type_id']

                # Параметризованный запрос
                sql1 = '''
                SELECT source_id, source_name, source_title, rss_url, source_photo
                FROM sources 
                WHERE channel_id = %(channel_id)s AND type_id = %(type_id)s
                '''
                cursor.execute(sql1, {'channel_id': channel_id, 'type_id': id_of_news_type})
                sources = cursor.fetchall()
                return sources
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_source_by_source_name(source_name):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                sql = 'SELECT * FROM sources WHERE source_name = %(source_name)s'
                cursor.execute(sql, {'source_name': source_name})
                source = cursor.fetchone()
            return dict(source) if source else None

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def update_sources_values(source_id: int, updates: dict):
        try:
            connection = connection_db()
            if connection is None:
                return DataFailedMessage(error_message='Ошибка в работе базы данных!')

            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                # Построение части запроса SET col1 = %(col1)s, col2 = %(col2)s ...
                set_clause = ', '.join([f"{key} = %({key})s" for key in updates.keys()])
                query = f"""
                    UPDATE sources
                    SET {set_clause}
                    WHERE source_id = %(source_id)s
                    RETURNING *;
                """
                # Добавляем source_id к параметрам
                updates['source_id'] = source_id
                cursor.execute(query, updates)
                connection.commit()
                return cursor.fetchone()
        except Exception as e:
            return {"error": str(e)}



chan_dal = SourceDAL()
# print(chan_dal.get_sources_by_channel_id(6))
# print(chan_dal.get_source_by_source_name('artemshumeiko'))