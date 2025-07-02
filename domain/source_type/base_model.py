from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
<<<<<<< HEAD
from sqlalchemy.orm import relationship, Mapped
from ..database import Base
=======
from sqlalchemy.orm import relationship
from ..base import Base
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6

class SourceType(Base):
    __tablename__ = 'source_types'
    type_id = Column(Integer, primary_key=True)
    type_name = Column(Text)

    source_type_sources: Mapped[list["Source"]] = relationship(back_populates='source_type')