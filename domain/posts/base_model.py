from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..db_manager import Base

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey('prompts.prompt_id'))
    image_id = Column(Integer, ForeignKey('images.image_id'))
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))
    source_id = Column(Integer, ForeignKey('sources.source_id'))
    content_text = Column(Text)
    created_at = Column(DateTime)
    published_at = Column(DateTime)
    scheduled_time = Column(DateTime)

    prompt = relationship("Prompt")
    image = relationship("Image")
    channel = relationship("Channel")
    source = relationship("Source")