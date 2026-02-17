import os
from pydantic_settings import BaseSettings

from functools import lru_cache
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "")

    model_config={
        "env_file": ".env",
        "extra": "ignore"
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()

