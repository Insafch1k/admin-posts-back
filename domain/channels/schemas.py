from pydantic import BaseModel

class ChannelSchema(BaseModel):
    channel_id: int
    channel_username: int
    channel_title: str
    created_at: datetime
    bot_id: int