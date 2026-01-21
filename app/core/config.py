"""
Core configuration module for FastAPI application.
Loads settings from environment variables using Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env
    )
    
    database_url: str = Field(
        default="postgresql://payment_user:your_secure_password_here@localhost:5432/payment_db",
        alias="DATABASE_URL"
    )


# Global settings instance
settings = Settings()
