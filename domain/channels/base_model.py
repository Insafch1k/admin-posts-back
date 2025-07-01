# domain/channels/base_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
from domain.prompts.base_model import Prompt
from domain.styles.base_model import Style



class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(String, nullable=False, unique=True)
    channel_photo = Column(String)
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey('botstorages.bot_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    prompts = relationship("Prompt", back_populates="channel")
    keywords = relationship("Keyword", back_populates="channel")