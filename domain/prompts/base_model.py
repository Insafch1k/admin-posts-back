from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class Prompt(Base):
    __tablename__ = 'prompts'
    prompt_id = Column(Integer, primary_key=True)
    prompt_text = Column(Text)
    style_id = Column(Integer, ForeignKey('styles.style_id'))
    source_id = Column(Integer, ForeignKey('sources.source_id'))
    created_at = Column(DateTime)

    style = relationship("Style")
    source = relationship("Source")