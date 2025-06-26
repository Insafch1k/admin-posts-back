from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    user_id: int
    tg_id: int
    name: Optional[str]
    login: Optional[str]
    password: Optional[str]