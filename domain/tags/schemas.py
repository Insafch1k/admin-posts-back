from pydantic import BaseModel

class TagSchema(BaseModel):
    tag_id: int
    tag_name: str