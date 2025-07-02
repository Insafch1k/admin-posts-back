from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped

from ..botstorages.base_model import BotStorage
from ..database import Base
from ..users.base_model import User


class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(Integer, primary_key=True)
    channel_username = Column(String, nullable=False)
    channel_title = Column(String)
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey(BotStorage.bot_id))
    user_id = Column(Integer, ForeignKey(User.user_id))

    channel_sources: Mapped[list["Source"]] = relationship(back_populates='source_channel')
    channel_bot: Mapped["BotStorage"] = relationship(back_populates='bot_channels')
    channel_user: Mapped["User"] = relationship(back_populates='user_channels')
    channel_schedules: Mapped[list["Schedule"]] = relationship(back_populates='schedule_channel')
