from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ScheduleSchema(BaseModel):
    schedule_id: int
    channel_id: int
    publish_time: datetime
    is_published: bool