from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class BotStorage(Base):
    __tablename__ = 'botstorages'
    bot_id = Column(Integer, primary_key=True)
    bot_key = Column(String)