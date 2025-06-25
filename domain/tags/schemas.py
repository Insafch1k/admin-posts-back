from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TagSchema(BaseModel):
    tag_id: int
    tag_name: str