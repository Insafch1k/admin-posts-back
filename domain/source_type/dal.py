from typing import Optional
import logging
from utils.database_manager import Executor, logger


class SourceTypeDAL(Executor):
    @staticmethod
    def get_type_id_by_name(type_name: str) -> Optional[int]:
        """Получает type_id по имени типа источника"""
        try:
            query = "SELECT type_id FROM source_type WHERE type_name = %s"
            result = Executor._execute_query(
                query=query,
                params=(type_name,),
                fetchone=True
            )
            return result["type_id"] if result else None
        except Exception as e:
            logger.error(f"Ошибка при получении type_id: {e}")
            return None

# res = SourceTypeDAL.get_type_id_by_name('Тг канал')
# print(res)