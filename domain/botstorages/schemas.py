from pydantic import BaseModel
from datetime import datetime

class BotStorageSchema(BaseModel):
    bot_id: int
    created_at: datetime