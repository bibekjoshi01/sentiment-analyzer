from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_name: str = "Sentiment Analyzer"
    app_version: str = "1.0.0"
    secret_key: str
    database_url: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
