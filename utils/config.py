# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     DB_NAME: str
#     USER: str
#     PASSWORD: str
#     PORT_NAME: str
#     HOST_NAME: str
#
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#         case_sensitive = True
#
#
# settings = Settings()

import os
import psycopg2

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_HOST: str
    API_ID : str
    API_HASH: str
    PHONE: str
    LOGIN: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    AUTH: str

    @property
    def DATABASE_URL_psycopg(self):
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


    # model_config = SettingsConfigDict(env_file='./.env')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
