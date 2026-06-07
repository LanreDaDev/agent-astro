"""Health check endpoint."""

from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from app.services.ephemeris import ephemeris_service

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API status and ephemeris availability.

    Returns:
        HealthCheckResponse with API status and ephemeris data availability
    """
    ephemeris_available = ephemeris_service.check_ephemeris_available()

    if ephemeris_available:
        return HealthCheckResponse(
            status="ok",
            ephemeris_available=True,
            message="API is running and ephemeris data is available",
        )
    else:
        return HealthCheckResponse(
            status="degraded",
            ephemeris_available=False,
            message="API is running but ephemeris data may not be available. "
            "Download Swiss Ephemeris data files to ephemeris_data/ directory.",
        )
