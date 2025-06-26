from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ImageSchema(BaseModel):
    image_id: int
    image_path: str