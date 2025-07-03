from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text

from sqlalchemy.orm import relationship, Mapped

from ..channels.base_model import Channel
from domain.base import Base
from ..source_type.base_model import SourceType

class Source(Base):
    __tablename__ = 'sources'
    source_id = Column(Integer, primary_key=True)
    source_name = Column(Text)
    source_title: Mapped[Optional[str]]
    source_photo: Mapped[Optional[str]]
    type_id = Column(Integer, ForeignKey(SourceType.type_id))
    channel_id = Column(Integer, ForeignKey(Channel.channel_id))

    source_last_news: Mapped[list["LastNews"]] = relationship(back_populates='last_news_source')
    source_type: Mapped["SourceType"] = relationship(back_populates='source_type_sources')
    source_channel: Mapped["Channel"] = relationship(back_populates='channel_sources')