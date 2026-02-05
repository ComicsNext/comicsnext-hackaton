from typing import Literal
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # App
    APP_NAME: str = "ComicsNext API"
    ENV: str = "dev"

    # Database (Azure SQL)
    AZURE_SQL_SERVER: str
    AZURE_SQL_DATABASE: str
    AZURE_SQL_USERNAME: str
    AZURE_SQL_PASSWORD: str

    # AI / RAG  👈 AQUÍ
    RAG_ENABLED: bool =  os.getenv("RAG_ENABLED", "false").lower() == "true"
    AI_PROVIDER: Literal["openai", "mock"] =  os.getenv("AI_PROVIDER", "mock").lower()  # "openai" o "mock"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Security / JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
