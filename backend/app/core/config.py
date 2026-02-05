from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ComicsNext API"
    ENV: str = "dev"

    # Database (Azure SQL)
    AZURE_SQL_SERVER: str
    AZURE_SQL_DATABASE: str
    AZURE_SQL_USERNAME: str
    AZURE_SQL_PASSWORD: str

    # Security / JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
