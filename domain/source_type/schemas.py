from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class SourceTypeSchema(BaseModel):
    type_id: int
    type_name: str