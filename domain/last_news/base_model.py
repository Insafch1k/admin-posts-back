from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from ..database import Base

class LastNews(Base):
    __tablename__ = 'lastnews'
    last_news_id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.source_id'))
    title = Column(Text)
    link = Column(Text)
    pub_date = Column(DateTime)
    decription = Column(Text)

    source = relationship("Source")

#qejhbfhebhjb