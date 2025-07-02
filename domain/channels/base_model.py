<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped

from ..botstorages.base_model import BotStorage
from ..database import Base
from ..users.base_model import User
=======
# domain/channels/base_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base
from domain.prompts.base_model import Prompt
from domain.styles.base_model import Style

>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6


class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(Integer, primary_key=True)
<<<<<<< HEAD
    channel_username = Column(String, nullable=False)
    channel_title = Column(String)
=======
    channel_username = Column(String, nullable=False, unique=True)
    channel_photo = Column(String)
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6
    created_at = Column(DateTime)
    bot_id = Column(Integer, ForeignKey(BotStorage.bot_id))
    user_id = Column(Integer, ForeignKey(User.user_id))

<<<<<<< HEAD
    channel_sources: Mapped[list["Source"]] = relationship(back_populates='source_channel')
    channel_bot: Mapped["BotStorage"] = relationship(back_populates='bot_channels')
    channel_user: Mapped["User"] = relationship(back_populates='user_channels')
    channel_schedules: Mapped[list["Schedule"]] = relationship(back_populates='schedule_channel')
=======
    prompts = relationship("Prompt", back_populates="channel")
    keywords = relationship("Keyword", back_populates="channel")
>>>>>>> eb0327c6c3c9fe18309d0233e06080c03a32a2d6
