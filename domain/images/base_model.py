from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from domain.base import Base

class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True)
    image_path = Column(Text)