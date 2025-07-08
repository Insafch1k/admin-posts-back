from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PostSchema(BaseModel):
    post_id: int
    prompt_id: int
    image_id: int
    channel_id: int
    content_text: str
    created_at: datetime
    published_at: Optional[datetime]
    scheduled_time: Optional[datetime]
    status: str
    content_name: str