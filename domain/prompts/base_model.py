from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from domain.base import Base
from ..sources.base_model import Source
from ..styles.base_model import Style

class Prompt(Base):
    __tablename__ = 'prompts'
    prompt_id = Column(Integer, primary_key=True)
    prompt_text = Column(Text)
    style_id = Column(Integer, ForeignKey(Style.style_id))
    source_id = Column(Integer, ForeignKey(Source.source_id))
    style_id = Column(Integer, ForeignKey('styles.style_id'))
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))
    created_at = Column(DateTime)

    channel = relationship("Channel", back_populates="prompts")
    style = relationship("Style", back_populates="prompts")