"""Planetary position endpoints."""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.models.schemas import (
    PlanetaryPositionRequest,
    PlanetaryPositionsResponse,
    PlanetPosition,
    DateTimeRequest,
    LocationRequest,
)
from app.services.calculator import calculator_service
from app.utils.time_converter import parse_datetime_with_timezone
from app.core.exceptions import (
    InvalidDateTimeError,
    InvalidLocationError,
    InvalidPlanetError,
    CalculationError,
    EphemerisDataError,
)

router = APIRouter()


@router.post("/planets/positions", response_model=PlanetaryPositionsResponse)
async def calculate_planetary_positions(request: PlanetaryPositionRequest):
    """
    Calculate positions for all major planets (or specified planets).

    Args:
        request: PlanetaryPositionRequest with datetime, location, and optional planet list

    Returns:
        PlanetaryPositionsResponse with calculated positions

    Example request:
        {
            "datetime": {
                "year": 2026,
                "month": 6,
                "day": 6,
                "hour": 12,
                "minute": 0
            },
            "location": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": "America/New_York"
            }
        }
    """
    try:
        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(request.datetime, request.location.timezone)

        # Calculate all planets
        planets = calculator_service.calculate_all_planets(
            dt, request.location.latitude, request.location.longitude
        )

        # Filter to specific planets if requested
        if request.planets:
            planets = [p for p in planets if p.planet in request.planets]

        return PlanetaryPositionsResponse(
            planets=planets,
            request_datetime=request.datetime,
            request_location=request.location,
        )

    except InvalidDateTimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidLocationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EphemerisDataError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except CalculationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/planets/{planet_name}/position", response_model=PlanetPosition)
async def get_single_planet_position(
    planet_name: str,
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    hour: int = Query(..., ge=0, le=23),
    minute: int = Query(..., ge=0, le=59),
    second: int = Query(default=0, ge=0, le=59),
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    timezone: str = Query(..., description="IANA timezone string"),
):
    """
    Calculate position for a single planet.

    Args:
        planet_name: Name of the planet (Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto)
        year: Year (1900-2100)
        month: Month (1-12)
        day: Day (1-31)
        hour: Hour (0-23)
        minute: Minute (0-59)
        second: Second (0-59)
        latitude: Latitude in degrees (-90 to 90)
        longitude: Longitude in degrees (-180 to 180)
        timezone: IANA timezone string (e.g., 'America/New_York')

    Returns:
        PlanetPosition with calculated position

    Example:
        GET /api/v1/planets/Sun/position?year=2026&month=6&day=6&hour=12&minute=0&latitude=40.7128&longitude=-74.0060&timezone=America/New_York
    """
    try:
        # Create datetime request
        dt_request = DateTimeRequest(
            year=year, month=month, day=day, hour=hour, minute=minute, second=second
        )

        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(dt_request, timezone)

        # Calculate planet position
        position = calculator_service.calculate_single_planet(
            planet_name, dt, latitude, longitude
        )

        return position

    except InvalidPlanetError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidDateTimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidLocationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EphemerisDataError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except CalculationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/planets/positions/now", response_model=PlanetaryPositionsResponse)
async def get_current_planetary_positions(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    timezone: str = Query(..., description="IANA timezone string"),
):
    """
    Calculate planetary positions for the current moment.

    Args:
        latitude: Latitude in degrees (-90 to 90)
        longitude: Longitude in degrees (-180 to 180)
        timezone: IANA timezone string (e.g., 'America/New_York')

    Returns:
        PlanetaryPositionsResponse with current positions

    Example:
        GET /api/v1/planets/positions/now?latitude=40.7128&longitude=-74.0060&timezone=America/New_York
    """
    try:
        # Get current time
        now = datetime.now()

        # Create datetime request from current time
        dt_request = DateTimeRequest(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
        )

        location_request = LocationRequest(
            latitude=latitude, longitude=longitude, timezone=timezone
        )

        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(dt_request, timezone)

        # Calculate all planets
        planets = calculator_service.calculate_all_planets(dt, latitude, longitude)

        return PlanetaryPositionsResponse(
            planets=planets,
            request_datetime=dt_request,
            request_location=location_request,
        )

    except InvalidDateTimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidLocationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EphemerisDataError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except CalculationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
