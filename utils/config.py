from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: str
    DB_HOST: str
    API_ID: int
    API_HASH: str
    PHONE: str
    LOGIN: str
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    AUTH: str

    class Config:
        env_file = find_dotenv()
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
