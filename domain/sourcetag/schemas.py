from pydantic import BaseModel

class SourceTagSchema(BaseModel):
    source_id: int
    tag_id: int