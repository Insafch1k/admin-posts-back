from sqlalchemy import Column, Integer, Text, ForeignKey
from domain.base import Base
from sqlalchemy.orm import relationship


class Keyword(Base):
    __tablename__ = 'keywords'

    keywords_id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey('channels.channel_id'), nullable=False)
    word = Column(Text, nullable=False)

    channel = relationship("Channel", back_populates="keywords")