"""
Application configuration using Pydantic Settings
"""
from functools import lru_cache
from typing import List, Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    app_name: str = "USGS Water Quality Reporting API"
    version: str = "1.0.0"
    environment: str = Field(default="development", env="ENV")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API Configuration
    api_prefix: str = "/api/v1"
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    
    # Database/Cache Configuration
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")
    
    # USGS API Configuration
    usgs_base_url: str = "https://waterqualitydata.us"
    max_records_per_request: int = 10000
    request_timeout: int = 30
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Monitoring
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()