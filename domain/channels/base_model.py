from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(Integer, nullable=False)
    channel_title = Column(String)
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey('botstorages.bot_id'))

    # Связи
    bot = relationship("BotStorage")