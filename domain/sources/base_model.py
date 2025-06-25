from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Source(Base):
    __tablename__ = 'sources'
    source_id = Column(Integer, primary_key=True)
    source_name = Column(Text)
    type_id = Column(Integer, ForeignKey('source_types.type_id'))
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))

    source_type = relationship("SourceType")
    channel = relationship("Channel")