"""
app/config.py
Centralised settings loaded from environment variables / .env file.

MongoDB Atlas connection string format:
  mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority

Code execution is handled by Piston (https://emkc.org/api/v2/piston)
— no API key required.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB Atlas
    mongodb_url: str = ""
    database_name: str = "codecritic"

    # Groq AI — FREE at https://console.groq.com
    groq_api_key: str = ""

    # App
    app_env: str = "development"
    secret_key: str = "change_me"
    cors_origins: str = "http://localhost:3000,https://codecritic-ai.onrender.com"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
