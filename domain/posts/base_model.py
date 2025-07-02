from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..channels.base_model import Channel
from ..database import Base
from ..images.base_model import Image
from ..prompts.base_model import Prompt
from ..sources.base_model import Source


class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    prompt_id = Column(Integer, ForeignKey(Prompt.prompt_id))
    image_id = Column(Integer, ForeignKey(Image.image_id))
    channel_id = Column(Integer, ForeignKey(Channel.channel_id))
    source_id = Column(Integer, ForeignKey(Source.source_id))
    content_text = Column(Text)
    created_at = Column(DateTime)
    published_at = Column(DateTime)
    scheduled_time = Column(DateTime)

    prompt = relationship("Prompt")
    image = relationship("Image")
    channel = relationship("Channel")
    source = relationship("Source")