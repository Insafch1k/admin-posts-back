from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Post(Base):
    __tablename__ = 'posts'
    post_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.source_id'))
    prompt_id = Column(Integer, ForeignKey('prompts.prompt_id'))
    image_id = Column(Integer, ForeignKey('images.image_id'))
    channel_id = Column(Integer, ForeignKey('channels.channel_id'))
    schedule_id = Column(Integer, ForeignKey('schedules.schedule_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    content_text = Column(String)
    created_at = Column(DateTime)
    published_at = Column(DateTime)
    scheduled_time = Column(DateTime)

    # Связи
    source = relationship("Source")
    prompt = relationship("Prompt")
    image = relationship("Image")
    channel = relationship("Channel")
    schedule = relationship("Schedule")
    user = relationship("User")