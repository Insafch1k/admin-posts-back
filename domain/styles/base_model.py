from sqlalchemy import Column, Integer, String
from ..database import Base

class Style(Base):
    __tablename__ = 'styles'
    style_id = Column(Integer, primary_key=True)
    parameters = Column(String)