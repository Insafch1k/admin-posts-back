from sqlalchemy import select

from domain.last_news import LastNews
from utils.connection_db import connection_db
from utils.data_state import DataFailedMessage


class LastNewsDAL():
    def get_last_news_by_source_id(self, source_id):
        Session = connection_db()
        if Session is None:
            return DataFailedMessage(error_message='Ошибка в работе базы данных!')

        with Session() as session:
            last_saved_news: LastNews = session.execute(
                select(LastNews).filter(LastNews.source_id == source_id).order_by(LastNews.message_id.desc())
            ).scalars().first()

        print(last_saved_news if last_saved_news else None)
        return last_saved_news if last_saved_news else None

lsd = LastNewsDAL()
lsd.get_last_news_by_source_id(1)