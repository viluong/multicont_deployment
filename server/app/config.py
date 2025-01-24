import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_user: str
    pg_host: str
    pg_database: str
    pg_password: str
    pg_port: int
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"

settings = Settings()