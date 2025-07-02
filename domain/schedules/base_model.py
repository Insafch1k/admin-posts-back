from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
<<<<<<< HEAD
from sqlalchemy.orm import relationship, Mapped

from ..channels.base_model import Channel
from ..database import Base
=======
from sqlalchemy.orm import relationship
from ..base import Base
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6

class Schedule(Base):
    __tablename__ = 'schedules'
    schedule_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey(Channel.channel_id))
    publish_time = Column(DateTime)
    is_published = Column(Boolean)

    schedule_channel: Mapped["Channel"] = relationship(back_populates='channel_schedules')