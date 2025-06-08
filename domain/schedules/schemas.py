from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScheduleSchema(BaseModel):
    schedule_id: int
    publish_time: Optional[datetime] = None
    is_published: bool
    channel_id: int