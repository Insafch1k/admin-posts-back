from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ChannelSchema(BaseModel):
    channel_id: int
    channel_username: int
    channel_title: int
    created_at: datetime
    bot_id: int
    user_id: int

class ChannelResponse(BaseModel):
    id: int = Field(alias="channel_id")  # Маппинг с channel_id
    name: str = Field(alias="channel_username")  # Берём из channel_username
    avatarUrl: str = Field(alias="channel_photo")  # Берём из channel_photo

    model_config = ConfigDict(  # Используем новый стиль конфигурации
        from_attributes=True,  # Бывший orm_mode
        populate_by_name=True  # Бывший allow_population_by_field_name
    )