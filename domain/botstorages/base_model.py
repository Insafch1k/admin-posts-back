from sqlalchemy import Column, Integer, DateTime
from ..database import Base

class BotStorage(Base):
    __tablename__ = 'botstorages'
    bot_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)