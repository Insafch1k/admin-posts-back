from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class StyleSchema(BaseModel):
    style_id: int
    parameters: str

    model_config = ConfigDict(from_attributes=True)