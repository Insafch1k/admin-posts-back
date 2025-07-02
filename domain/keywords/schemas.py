from pydantic import BaseModel, ConfigDict


class KeywordSchema(BaseModel):
    keywords_id: int
    channel_id: int
    word: str

    model_config = ConfigDict(from_attributes=True)