from sqlalchemy import Column, Integer, String
from ..database import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False)