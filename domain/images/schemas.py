from pydantic import BaseModel

class ImageSchema(BaseModel):
    image_id: int
    image_url: str