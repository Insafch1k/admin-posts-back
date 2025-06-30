from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..db_manager import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    name = Column(Text)
    login = Column(Text)
    password = Column(Text)