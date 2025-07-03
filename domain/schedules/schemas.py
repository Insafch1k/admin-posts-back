from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ScheduleSchema(BaseModel):
    schedule_id: int
    channel_id: int
    post_id: int
    publish_time: datetime
    published_at: Optional[datetime]