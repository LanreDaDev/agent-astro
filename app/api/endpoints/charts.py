"""Chart calculation endpoints (houses, natal charts)."""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    NatalChartRequest,
    NatalChartResponse,
    HousesResponse,
    HouseCusp,
    PlanetaryPositionRequest,
)
from app.services.calculator import calculator_service
from app.utils.time_converter import parse_datetime_with_timezone
from app.core.exceptions import (
    InvalidDateTimeError,
    InvalidLocationError,
    CalculationError,
    EphemerisDataError,
)
from app.core.constants import HOUSE_SYSTEMS

router = APIRouter()


@router.post("/charts/houses", response_model=HousesResponse)
async def calculate_houses(request: PlanetaryPositionRequest):
    """
    Calculate astrological houses for a given time and location.

    Args:
        request: Request with datetime, location, and house system

    Returns:
        HousesResponse with house cusps and important angles

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
            },
            "house_system": "P"
        }
    """
    try:
        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(request.datetime, request.location.timezone)

        # Calculate houses
        houses_data = calculator_service.calculate_houses(
            dt, request.location.latitude, request.location.longitude, request.house_system
        )

        # Format house cusps
        house_cusps = []
        for i, cusp_longitude in enumerate(houses_data["house_cusps"], start=1):
            # Get zodiac sign and degree for this cusp
            sign, degree = calculator_service.ephemeris.longitude_to_zodiac(cusp_longitude)
            house_cusps.append(
                HouseCusp(
                    house_number=i,
                    longitude=cusp_longitude,
                    zodiac_sign=sign,
                    zodiac_degree=degree,
                )
            )

        return HousesResponse(
            house_cusps=house_cusps,
            ascendant=houses_data["ascendant"],
            midheaven=houses_data["midheaven"],
            vertex=houses_data["vertex"],
            house_system=houses_data["house_system"],
            house_system_name=HOUSE_SYSTEMS.get(houses_data["house_system"], "Unknown"),
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


@router.post("/charts/natal", response_model=NatalChartResponse)
async def calculate_natal_chart(request: NatalChartRequest):
    """
    Calculate a complete natal chart with planets and houses.

    Args:
        request: Request with datetime, location, house system, and options

    Returns:
        NatalChartResponse with complete chart information

    Example request:
        {
            "datetime": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14,
                "minute": 30
            },
            "location": {
                "latitude": 51.5074,
                "longitude": -0.1278,
                "timezone": "Europe/London"
            },
            "house_system": "P",
            "include_houses": true
        }
    """
    try:
        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(request.datetime, request.location.timezone)

        # Calculate natal chart
        chart_data = calculator_service.calculate_natal_chart(
            dt,
            request.location.latitude,
            request.location.longitude,
            request.house_system,
            request.include_houses,
            request.include_all_bodies,
        )

        # Format houses response if included
        houses_response = None
        if request.include_houses and chart_data["houses"]:
            houses_data = chart_data["houses"]
            house_cusps = []
            for i, cusp_longitude in enumerate(houses_data["house_cusps"], start=1):
                sign, degree = calculator_service.ephemeris.longitude_to_zodiac(cusp_longitude)
                house_cusps.append(
                    HouseCusp(
                        house_number=i,
                        longitude=cusp_longitude,
                        zodiac_sign=sign,
                        zodiac_degree=degree,
                    )
                )

            houses_response = HousesResponse(
                house_cusps=house_cusps,
                ascendant=houses_data["ascendant"],
                midheaven=houses_data["midheaven"],
                vertex=houses_data["vertex"],
                house_system=houses_data["house_system"],
                house_system_name=HOUSE_SYSTEMS.get(houses_data["house_system"], "Unknown"),
                request_datetime=request.datetime,
                request_location=request.location,
            )

        return NatalChartResponse(
            planets=chart_data["planets"],
            houses=houses_response,
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
