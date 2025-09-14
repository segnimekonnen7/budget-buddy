"""Configuration settings for the application."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Database - Use SQLite for local development
    postgres_url: str = "sqlite:///./habitloop.db"
    
    # CORS - Updated for GitHub Pages deployment with environment variable support
    cors_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://segnimekonnen7.github.io")
    allowed_origins: List[str] = [origin.strip() for origin in cors_env.split(",")]
    
    # Debug logging
    print(f"DEBUG: CORS origins loaded: {allowed_origins}")
    print(f"DEBUG: Environment variable ALLOWED_ORIGINS: {cors_env}")
    
    # Email
    sendgrid_api_key: Optional[str] = None
    alerts_from_email: str = "alerts@habitloop.local"
    app_base_url: str = "http://localhost:3000"
    
    # Auth
    jwt_secret: str = "please-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days
    
    # Scheduler
    scheduler_interval_minutes: int = 15
    
    # Bandit
    bandit_epsilon: float = 0.1
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()