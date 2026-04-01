from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"
    MINIO_URL: str = "http://localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "avatars"
    ENV: str = "development"
    VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")

settings = Settings()

DB_URL = settings.DB_URL
MINIO_URL = settings.MINIO_URL
MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME
ENV = settings.ENV
VERSION = settings.VERSION
