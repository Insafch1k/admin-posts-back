from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StyleSchema(BaseModel):
    style_id: int
    parameters: str