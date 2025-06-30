# domain/channels/base_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..db_manager import Base
from ..botstorages import BotStorage
from ..users import User


class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(String, nullable=False, unique=True)
    channel_photo = Column(String)
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey('botstorages.bot_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    bot = relationship("BotStorage")
    user = relationship("User")