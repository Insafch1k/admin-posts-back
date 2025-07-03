from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped
from domain.base import Base


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    name = Column(Text)
    login = Column(Text)
    password = Column(Text)

    user_channels: Mapped[list["Channel"]] = relationship(back_populates='channel_user')