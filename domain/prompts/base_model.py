from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Prompt(Base):
    __tablename__ = 'prompts'
    prompt_id = Column(Integer, primary_key=True)
    prompt_text = Column(String, nullable=False)
    style_id = Column(Integer, ForeignKey('styles.style_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime)

    # Связи
    style = relationship("Style")
    user = relationship("User")