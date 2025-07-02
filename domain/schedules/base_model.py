from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped

from ..channels.base_model import Channel
from ..database import Base

class Schedule(Base):
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey(Channel.channel_id))
    publish_time = Column(DateTime)
    is_published = Column(Boolean)

    schedule_channel: Mapped["Channel"] = relationship(back_populates='channel_schedules')