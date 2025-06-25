from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PromptSchema(BaseModel):
    prompt_id: int
    prompt_text: str
    style_id: int
    source_id: int
    created_at: datetime