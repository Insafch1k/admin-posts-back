from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..base import Base

class Schedule(Base):
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))
    publish_time = Column(DateTime)
    is_published = Column(Boolean)

    channel = relationship("Channel")