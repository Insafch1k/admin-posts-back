from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped
from domain.base import Base

class SourceType(Base):
    __tablename__ = 'source_types'
    type_id = Column(Integer, primary_key=True)
    type_name = Column(Text)

    source_type_sources: Mapped[list["Source"]] = relationship(back_populates='source_type')