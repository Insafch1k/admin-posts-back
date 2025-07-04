from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SourceSchema(BaseModel):
    source_id: int
    source_name: str
    type_id: int
    channel_id: int