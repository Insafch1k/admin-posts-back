from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
<<<<<<< HEAD
from domain.database import Base
=======
from ..base import Base
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6

class Image(Base):
    __tablename__ = 'images'

    image_id = Column(Integer, primary_key=True)
    image_path = Column(Text)