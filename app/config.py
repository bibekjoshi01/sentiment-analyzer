from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Sentiment Analyzer"
    app_version: str = "1.0.0"
    secret_key: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
