from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
<<<<<<< HEAD
from sqlalchemy.orm import relationship, Mapped
from ..database import Base
=======
from sqlalchemy.orm import relationship
from ..base import Base
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6

class BotStorage(Base):
    __tablename__ = 'botstorages'
    bot_id = Column(Integer, primary_key=True)
    bot_key = Column(String)

    bot_channels: Mapped[list["Channel"]] = relationship(back_populates='channel_bot')