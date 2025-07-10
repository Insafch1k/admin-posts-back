from typing import Optional, Dict, Any, Union
from domain.source_type.dal import SourceTypeDAL
from utils.data_state import DataFailedMessage
from utils.database_manager import Executor, logger


class SourceDAL(Executor):
    @staticmethod
    def get_sources_by_channel_id(channel_id: int, type_name):
        try:
            type_id = SourceTypeDAL.get_type_id_by_name(type_name)
            if type_id is None:
                print("❌ Не найден тип 'Тг канал'")
                return []

            query = """
                    SELECT source_id, source_name, source_title, rss_url, source_photo
                    FROM sources
                    WHERE channel_id = %s AND type_id = %s
                """
            sources = Executor._execute_query(
                query=query,
                params=(channel_id, type_id),
                fetchall=True
            )
            return sources or []

        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_source_by_source_name(source_name: str) -> Optional[Union[Dict, None]]:
        """Получить источник по названию источника"""
        try:
            query = 'SELECT * FROM sources WHERE source_name = %s'
            result = Executor._execute_query(
                query=query,
                params=(source_name,),
                fetchone=True
            )
            return result if result else None

        except Exception as e:
            logger.error(f"Ошибка при получении источника: {e}")
            return {"error": str(e)}

    @staticmethod
    def update_sources_values(source_id: int, updates: dict) -> Union[Dict[str, Any], DataFailedMessage, None]:

        try:
            if not updates:
                raise ValueError("Нет данных для обновления.")

            set_clause = ', '.join([f"{key} = %({key})s" for key in updates.keys()])
            query = f"""
                    UPDATE sources
                    SET {set_clause}
                    WHERE source_id = %(source_id)s
                    RETURNING *;
                """

            updates['source_id'] = source_id
            result = Executor._execute_query(
                query=query,
                params=updates,
                fetchone=True
            )
            return result if result else None

        except Exception as e:
            logger.error(f"Ошибка при обновлении источника: {e}")
            return {"error": str(e)}

    @staticmethod
    def add_source(data: dict) -> Union[int, Dict[str, str]]:
        try:
            if not data:
                raise ValueError("Нет допустимых полей для вставки.")

            fields = list(data.keys())
            values = [data[field] for field in fields]
            placeholders = ', '.join(['%s'] * len(fields))

            query = f"""
                    INSERT INTO sources ({', '.join(fields)})
                    VALUES ({placeholders})
                    RETURNING source_id;
                """
            print(data, query)
            result = Executor._execute_query(
                query=query,
                params=tuple(values),
                fetchone=True
            )
            return result['source_id'] if result else None

        except Exception as e:
            logger.error(f"Ошибка при добавлении источника: {e}")
            return {"error": str(e)}

    @staticmethod
    def delete_source(source_id: int) -> Union[str, Dict[str, str]]:
        try:
            query = """
                    DELETE FROM sources
                    WHERE source_id = %(source_id)s;
                """

            Executor._execute_query(
                query=query,
                params={'source_id': source_id}
            )
            return f"Источник {source_id} был удалён!"

        except Exception as e:
            logger.error(f"Ошибка при удалении источника: {e}")
            return {"error": str(e)}


# print(SourceDAL.get_sources_by_channel_id(6,'RSS лента'))
