from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..base import Base

class Style(Base):
    __tablename__ = 'styles'
    style_id = Column(Integer, primary_key=True)
    parameters = Column(Text)