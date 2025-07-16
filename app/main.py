"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse

from app.api import health, water_quality
from app.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for querying USGS Water Quality Portal data and generating reports",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(water_quality.router, prefix="/water-quality", tags=["water-quality"])
# Route included in water quality definition
# app.include_router(sites.router, prefix="/sites", tags=["sites"])

@app.get("/", response_class=HTMLResponse)
async def root():
    """API documentation homepage"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>USGS Water Quality Portal API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .method { color: #2196F3; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>USGS Water Quality Portal API</h1>
        <p>This API provides access to USGS Water Quality Portal data with report generation capabilities.</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code>
            <p>Check API health status</p>
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/water-quality/query</code>
            <p>Query water quality data and generate reports</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/water-quality/sites</code>
            <p>Get monitoring sites information</p>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/water-quality/parameters</code>
            <p>Get available water quality parameters</p>
        </div>
        
        <p><a href="/docs">View OpenAPI Documentation</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)