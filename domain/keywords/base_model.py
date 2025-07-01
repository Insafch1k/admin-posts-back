from sqlalchemy import Column, Integer, Text, ForeignKey
from domain.base import Base


class Keyword(Base):
    __tablename__ = 'keywords'

    keywords_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('channels.channel_id'), nullable=False)
    word = Column(Text, nullable=False)

    __table_args__ = (
        {'schema': 'public'},
        # Уникальное ограничение
        UniqueConstraint('channel_id', 'word', name='unique_channel_word')
    )