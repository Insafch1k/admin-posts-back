from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ChannelSchema(BaseModel):
    channel_id: int
    channel_username: int
    channel_title: int
    created_at: datetime
    bot_id: int
    user_id: int