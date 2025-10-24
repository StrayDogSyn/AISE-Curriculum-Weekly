"""
Application configuration module.

Manages environment variables and application settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses pydantic-settings for validation and type conversion.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application
    app_name: str = "FastAPI Boilerplate"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    allowed_origins: List[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    # Database (uncomment if needed)
    # database_url: str = "sqlite:///./test.db"
    
    # Security (uncomment if needed)
    # secret_key: str = "your-secret-key-change-this"
    # algorithm: str = "HS256"
    # access_token_expire_minutes: int = 30


# Create global settings instance
settings = Settings()
