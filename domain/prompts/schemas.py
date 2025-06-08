from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromptSchema(BaseModel):
    prompt_id: int
    prompt_text: str
    style_id: Optional[int] = None
    user_id: int
    created_at: datetime