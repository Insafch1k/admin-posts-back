from sqlalchemy import Column, Integer, String
from ..database import Base

class Image(Base):
    __tablename__ = 'images'
    image_id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False)