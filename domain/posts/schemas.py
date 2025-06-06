from pydantic import BaseModel

class PostSchema(BaseModel):
    post_id: int
    source_id: int
    prompt_id: int
    image_id: int
    channel_id: int
    schedule_id: int
    user_id: int
    content_text: str
    created_at: datetime
    published_at: Optional[datetime]
    scheduled_time: Optional[datetime]