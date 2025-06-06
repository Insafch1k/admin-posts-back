from pydantic import BaseModel

class SourceSchema(BaseModel):
    source_id: int
    source_name: str