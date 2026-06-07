"""Application configuration using Pydantic settings."""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "Astrology API"
    api_v1_prefix: str = "/api/v1"
    ephemeris_path: str = "./ephemeris_data"
    default_house_system: str = "P"
    enable_cors: bool = True
    allowed_origins: List[str] = ["*"]
    log_level: str = "INFO"


settings = Settings()
