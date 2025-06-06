from pydantic import BaseModel

class StyleSchema(BaseModel):
    style_id: int
    parameters: str