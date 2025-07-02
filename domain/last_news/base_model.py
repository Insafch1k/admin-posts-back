from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped
from domain.base import Base
from domain.sources.base_model import Source


class LastNews(Base):
    __tablename__ = 'lastnews'
    last_news_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey(Source.source_id))
    title = Column(Text)
    link = Column(Text)
    pub_date = Column(DateTime)
    description = Column(Text)
    photo: Mapped[Optional[str]]
    message_id: Mapped[Optional[int]]

    last_news_source: Mapped["Source"] = relationship(back_populates='source_last_news')

    repr_cols_num = 2

