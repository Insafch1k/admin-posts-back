from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class SourceType(Base):
    __tablename__ = 'source_types'
    type_id = Column(Integer, primary_key=True)
    type_name = Column(Text)