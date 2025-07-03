from sqlalchemy import select, and_

from domain.source_type.base_model import SourceType
from domain.sources.base_model import Source
from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage


class SourecDAL:
    def get_sources_by_channel_id(self, channel_id: int):  # ← добавлен self
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка в работе базы данных!')

        with Session() as session:
            if session is None:
                print("❌ Ошибка инициализации БД")
                return []

            result = session.execute(
                select(SourceType.type_id).filter(SourceType.type_name == 'Тг канал')
            ).scalar()

            if result is None:
                print("❌ Не найден тип 'Тг канал'")
                return []

            id_of_news_type = result

            stmt = select(Source.source_id, Source.source_name).filter(
                and_(
                    Source.channel_id == channel_id,
                    Source.type_id == id_of_news_type
                )
            )

            sources = session.execute(stmt).all()
            return [{"id": s.source_id, "name": s.source_name} for s in sources]

    def get_source_by_source_name(self, source_name):
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка в работе базы данных!')

        with Session() as session:
            source = session.execute(
                select(Source).filter(Source.source_name == source_name)
            ).scalars().first()
        return source if source else None


chan_dal = SourecDAL()
print(chan_dal.get_sources_by_channel_id(1))