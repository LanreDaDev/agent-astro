"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.ephemeris import ephemeris_service
from app.api.endpoints import health, planets, charts, location, aspects


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize ephemeris
    ephemeris_service.initialize(settings.ephemeris_path)
    yield
    # Shutdown: Clean up if needed
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Astrology API for calculating planetary positions using Swiss Ephemeris",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["Health"])
app.include_router(planets.router, prefix=settings.api_v1_prefix, tags=["Planets"])
app.include_router(charts.router, prefix=settings.api_v1_prefix, tags=["Charts"])
app.include_router(location.router, prefix=settings.api_v1_prefix, tags=["Location"])
app.include_router(aspects.router, prefix=settings.api_v1_prefix, tags=["Aspects"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to the Astrology API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": f"{settings.api_v1_prefix}/health",
    }
