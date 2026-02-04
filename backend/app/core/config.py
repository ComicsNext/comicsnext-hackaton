from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str = "dev"

    database_url: str

    default_page_size: int = 10
    max_page_size: int = 50

    class Config:
        env_file = ".env"


settings = Settings()
