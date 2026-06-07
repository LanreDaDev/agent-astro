"""Aspects calculation endpoints."""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import (
    AspectsRequest,
    AspectsResponse,
    Aspect,
    TransitAspectsRequest,
    TransitAspectsResponse,
    DateTimeRequest,
)
from app.services.calculator import calculator_service
from app.services.aspects import aspect_service
from app.utils.time_converter import parse_datetime_with_timezone
from app.core.exceptions import (
    InvalidDateTimeError,
    InvalidLocationError,
    CalculationError,
    EphemerisDataError,
)

router = APIRouter()


@router.post("/aspects", response_model=AspectsResponse)
async def calculate_aspects(request: AspectsRequest):
    """
    Calculate all major aspects in a natal chart.

    This endpoint calculates aspects (conjunctions, oppositions, trines, squares, sextiles)
    between all planets in the chart.

    Args:
        request: AspectsRequest with datetime, location, and options

    Returns:
        AspectsResponse with all calculated aspects

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
            "include_all_bodies": false,
            "custom_orbs": {
                "conjunction": 10.0,
                "trine": 8.0
            }
        }
    """
    try:
        # Parse datetime with timezone
        dt = parse_datetime_with_timezone(request.datetime, request.location.timezone)

        # Calculate planets
        if request.include_all_bodies:
            planets = calculator_service.calculate_all_bodies(
                dt, request.location.latitude, request.location.longitude
            )
        else:
            planets = calculator_service.calculate_all_planets(
                dt, request.location.latitude, request.location.longitude
            )

        # Convert to list of dicts for aspect calculation
        planet_data = [
            {
                "planet": p.planet,
                "longitude": p.longitude,
            }
            for p in planets
        ]

        # Calculate aspects
        aspects_data = aspect_service.calculate_all_aspects(
            planet_data,
            custom_orbs=request.custom_orbs,
            include_minor=request.include_minor_aspects
        )

        # Convert to Aspect models
        aspects = [Aspect(**aspect) for aspect in aspects_data]

        return AspectsResponse(
            aspects=aspects,
            total_aspects=len(aspects),
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


@router.post("/transits", response_model=TransitAspectsResponse)
async def calculate_transit_aspects(request: TransitAspectsRequest):
    """
    Calculate transit aspects (current/transiting planets aspecting natal planets).

    This endpoint shows how current planetary positions aspect your natal chart.
    Perfect for understanding what planetary influences are active in your life right now!

    Args:
        request: TransitAspectsRequest with natal and transit information

    Returns:
        TransitAspectsResponse with all transit aspects

    Example request:
        {
            "natal_datetime": {
                "year": 1990,
                "month": 5,
                "day": 15,
                "hour": 14,
                "minute": 30
            },
            "natal_location": {
                "latitude": 51.5074,
                "longitude": -0.1278,
                "timezone": "Europe/London"
            },
            "transit_datetime": null,  // Uses current time
            "include_minor_aspects": true
        }
    """
    try:
        # Parse natal datetime
        natal_dt = parse_datetime_with_timezone(
            request.natal_datetime,
            request.natal_location.timezone
        )

        # Determine transit datetime (use current if not provided)
        if request.transit_datetime:
            transit_dt_request = request.transit_datetime
            transit_loc = request.transit_location or request.natal_location
            transit_dt = parse_datetime_with_timezone(
                transit_dt_request,
                transit_loc.timezone
            )
        else:
            # Use current time
            now = datetime.now()
            transit_dt_request = DateTimeRequest(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=now.hour,
                minute=now.minute,
                second=now.second
            )
            transit_loc = request.natal_location
            transit_dt = parse_datetime_with_timezone(
                transit_dt_request,
                transit_loc.timezone
            )

        # Calculate natal planets
        if request.include_all_bodies:
            natal_planets = calculator_service.calculate_all_bodies(
                natal_dt,
                request.natal_location.latitude,
                request.natal_location.longitude
            )
        else:
            natal_planets = calculator_service.calculate_all_planets(
                natal_dt,
                request.natal_location.latitude,
                request.natal_location.longitude
            )

        # Calculate transit planets
        if request.include_all_bodies:
            transit_planets = calculator_service.calculate_all_bodies(
                transit_dt,
                transit_loc.latitude,
                transit_loc.longitude
            )
        else:
            transit_planets = calculator_service.calculate_all_planets(
                transit_dt,
                transit_loc.latitude,
                transit_loc.longitude
            )

        # Convert to dicts for aspect calculation (include speed and retrograde)
        natal_data = [
            {
                "planet": p.planet,
                "longitude": p.longitude,
                "speed": p.speed,
                "retrograde": p.retrograde
            }
            for p in natal_planets
        ]
        transit_data = [
            {
                "planet": p.planet,
                "longitude": p.longitude,
                "speed": p.speed,
                "retrograde": p.retrograde
            }
            for p in transit_planets
        ]

        # Calculate transit aspects
        aspects_data = aspect_service.calculate_transit_aspects(
            natal_data,
            transit_data,
            custom_orbs=request.custom_orbs,
            include_minor=request.include_minor_aspects
        )

        # Convert to Aspect models
        aspects = [Aspect(**aspect) for aspect in aspects_data]

        return TransitAspectsResponse(
            aspects=aspects,
            total_aspects=len(aspects),
            natal_datetime=request.natal_datetime,
            natal_location=request.natal_location,
            transit_datetime=transit_dt_request,
            transit_location=transit_loc,
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
