"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api import health, water_quality, sites
from app.core.config import get_settings
from app.utils.logging import setup_logging
from app.utils.monitoring import add_monitoring_middleware

# Initialize settings
settings = get_settings()

# Setup logging
setup_logging(settings.log_level)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="USGS Water Quality Portal API",
    version=settings.version,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
add_monitoring_middleware(app)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(water_quality.router, prefix="/water-quality", tags=["water-quality"])
app.include_router(sites.router, prefix="/sites", tags=["sites"])