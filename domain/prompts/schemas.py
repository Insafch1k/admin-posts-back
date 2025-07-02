from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class PromptSchema(BaseModel):
    prompt_id: int
    prompt_text: str
    style_id: int
    channel_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)