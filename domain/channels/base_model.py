from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(Integer, nullable=False)
    channel_title = Column(Integer)
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey('botstorages.bot_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    bot = relationship("BotStorage")
    user = relationship("User")