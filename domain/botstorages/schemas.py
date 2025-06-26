from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class BotStorageSchema(BaseModel):
    bot_id: int
    bot_key: str