"""Location lookup endpoint."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from app.services.location_lookup import location_lookup_service
from app.core.exceptions import InvalidLocationError

router = APIRouter()


class LocationResponse(BaseModel):
    """Response from location lookup."""

    address: str = Field(..., description="Full address of the location")
    latitude: float = Field(..., description="Latitude in decimal degrees")
    longitude: float = Field(..., description="Longitude in decimal degrees")
    timezone: str = Field(..., description="IANA timezone string")


@router.get("/location/lookup", response_model=LocationResponse)
async def lookup_location(
    query: str = Query(
        ...,
        description="Location name (e.g., 'New York', 'London, UK', 'Paris, France')",
        min_length=2,
    )
):
    """
    Look up coordinates and timezone for a location name.

    This endpoint uses OpenStreetMap's Nominatim service to geocode location names
    and returns the coordinates and IANA timezone.

    Args:
        query: Location name to search for

    Returns:
        LocationResponse with address, coordinates, and timezone

    Example:
        GET /api/v1/location/lookup?query=New York, NY

    Response:
        {
            "address": "New York, United States",
            "latitude": 40.7127281,
            "longitude": -74.0060152,
            "timezone": "America/New_York"
        }
    """
    try:
        result = location_lookup_service.lookup_location(query)
        return LocationResponse(**result)
    except InvalidLocationError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
