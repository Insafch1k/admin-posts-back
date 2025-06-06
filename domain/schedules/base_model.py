from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Schedule(Base):
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    publish_time = Column(DateTime)
    is_published = Column(Boolean, default=False)

    # Связи
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))
    channel = relationship("Channel")