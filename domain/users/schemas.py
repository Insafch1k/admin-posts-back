from pydantic import BaseModel

class UserSchema(BaseModel):
    user_id: int
    tg_id: int
    name: str