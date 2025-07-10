from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SourceSchemaOut(BaseModel):
    source_id: int
    source_name: str
    source_title: str
    rss_url: Optional[str] = None
    source_photo: Optional[str] = None
    subscribers: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
