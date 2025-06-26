from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class LastNewsSchema(BaseModel):
    last_news_id: int
    source_id: int
    title: str
    link: str
    pub_date: datetime
    decription: str

#jaebrjkbearjkebnkj