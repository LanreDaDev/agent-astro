"""Pydantic models for request and response validation."""

from typing import List, Optional, Dict
from datetime import datetime as dt
from pydantic import BaseModel, Field, field_validator
import pytz


class DateTimeRequest(BaseModel):
    """Date and time components for astrological calculations."""

    year: int = Field(..., ge=1900, le=2100, description="Year (1900-2100)")
    month: int = Field(..., ge=1, le=12, description="Month (1-12)")
    day: int = Field(..., ge=1, le=31, description="Day (1-31)")
    hour: int = Field(..., ge=0, le=23, description="Hour (0-23)")
    minute: int = Field(..., ge=0, le=59, description="Minute (0-59)")
    second: int = Field(default=0, ge=0, le=59, description="Second (0-59)")

    @field_validator("day")
    @classmethod
    def validate_day(cls, v: int, info) -> int:
        """Validate day is valid for the given month."""
        if info.data.get("month") in [4, 6, 9, 11] and v > 30:
            raise ValueError(f"Month {info.data['month']} only has 30 days")
        if info.data.get("month") == 2 and v > 29:
            raise ValueError("February only has 28 or 29 days")
        return v


class LocationRequest(BaseModel):
    """Geographic location for astrological calculations."""

    latitude: float = Field(
        ..., ge=-90, le=90, description="Latitude in degrees (-90 to 90)"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Longitude in degrees (-180 to 180)"
    )
    timezone: str = Field(..., description="IANA timezone string (e.g., 'America/New_York')")

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone string against pytz database."""
        try:
            pytz.timezone(v)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Invalid timezone: {v}")
        return v


class PlanetaryPositionRequest(BaseModel):
    """Request for calculating planetary positions."""

    datetime: DateTimeRequest
    location: LocationRequest
    planets: Optional[List[str]] = Field(
        default=None,
        description="List of planets to calculate (if None, returns all major planets)",
    )
    house_system: str = Field(
        default="P", description="House system code (P=Placidus, K=Koch, etc.)"
    )


class PlanetPosition(BaseModel):
    """Calculated position of a planet."""

    planet: str = Field(..., description="Planet name")
    longitude: float = Field(..., description="Absolute longitude (0-360 degrees)")
    latitude: float = Field(..., description="Ecliptic latitude")
    distance: float = Field(..., description="Distance from Earth in AU")
    speed: float = Field(..., description="Daily motion in degrees")
    zodiac_sign: str = Field(..., description="Zodiac sign the planet is in")
    zodiac_degree: float = Field(
        ..., description="Degree within the zodiac sign (0-30)"
    )
    retrograde: bool = Field(..., description="Whether the planet is in retrograde motion")
    house: Optional[int] = Field(
        default=None, description="House number (for future implementation)"
    )


class PlanetaryPositionsResponse(BaseModel):
    """Response containing calculated planetary positions."""

    planets: List[PlanetPosition]
    calculated_at: dt = Field(
        default_factory=dt.utcnow, description="Timestamp when calculation was performed"
    )
    request_datetime: DateTimeRequest
    request_location: LocationRequest


class HouseCusp(BaseModel):
    """A single house cusp."""

    house_number: int = Field(..., ge=1, le=12, description="House number (1-12)")
    longitude: float = Field(..., description="Cusp longitude (0-360 degrees)")
    zodiac_sign: str = Field(..., description="Zodiac sign of the cusp")
    zodiac_degree: float = Field(..., description="Degree within the zodiac sign (0-30)")


class HousesResponse(BaseModel):
    """Response containing house calculations."""

    house_cusps: List[HouseCusp] = Field(..., description="12 house cusps")
    ascendant: float = Field(..., description="Ascendant (1st house cusp)")
    midheaven: float = Field(..., description="Midheaven (10th house cusp)")
    vertex: float = Field(..., description="Vertex point")
    house_system: str = Field(..., description="House system used")
    house_system_name: str = Field(..., description="Full name of house system")
    calculated_at: dt = Field(
        default_factory=dt.utcnow, description="Timestamp when calculation was performed"
    )
    request_datetime: DateTimeRequest
    request_location: LocationRequest


class NatalChartRequest(BaseModel):
    """Request for a complete natal chart calculation."""

    datetime: DateTimeRequest
    location: LocationRequest
    house_system: str = Field(
        default="P", description="House system code (P=Placidus, K=Koch, etc.)"
    )
    include_houses: bool = Field(
        default=True, description="Whether to include house calculations"
    )
    include_all_bodies: bool = Field(
        default=False,
        description="Whether to include all bodies (asteroids, nodes, calculated points). If False, returns only the 10 major planets."
    )


class NatalChartResponse(BaseModel):
    """Response containing a complete natal chart."""

    planets: List[PlanetPosition]
    houses: Optional[HousesResponse] = Field(
        default=None, description="House information (if requested)"
    )
    calculated_at: dt = Field(
        default_factory=dt.utcnow, description="Timestamp when calculation was performed"
    )
    request_datetime: DateTimeRequest
    request_location: LocationRequest


class Aspect(BaseModel):
    """An astrological aspect between two planets."""

    planet1: str = Field(..., description="First planet in the aspect")
    planet2: str = Field(..., description="Second planet in the aspect")
    aspect: str = Field(..., description="Type of aspect (conjunction, trine, square, etc.)")
    angle: float = Field(..., description="Exact angle of this aspect type (0, 60, 90, 120, 180, 51.43 for septile, etc.)")
    orb: float = Field(..., description="Orb (deviation from exact aspect in degrees)")
    planet1_longitude: float = Field(..., description="Longitude of first planet")
    planet2_longitude: float = Field(..., description="Longitude of second planet")
    applying: Optional[bool] = Field(default=None, description="Whether aspect is applying (getting tighter). None if not calculated.")
    planet1_retrograde: Optional[bool] = Field(default=None, description="Whether planet1 is retrograde")
    planet2_retrograde: Optional[bool] = Field(default=None, description="Whether planet2 is retrograde")


class AspectsRequest(BaseModel):
    """Request for calculating aspects in a chart."""

    datetime: DateTimeRequest
    location: LocationRequest
    include_all_bodies: bool = Field(
        default=False,
        description="Whether to include all bodies or just major planets"
    )
    include_minor_aspects: bool = Field(
        default=False,
        description="Whether to include minor aspects (semi-sextile, quintile, etc.)"
    )
    custom_orbs: Optional[Dict[str, float]] = Field(
        default=None,
        description="Custom orbs for aspects (e.g., {'conjunction': 10.0, 'trine': 8.0})"
    )


class AspectsResponse(BaseModel):
    """Response containing calculated aspects."""

    aspects: List[Aspect]
    total_aspects: int = Field(..., description="Total number of aspects found")
    request_datetime: DateTimeRequest
    request_location: LocationRequest
    calculated_at: dt = Field(
        default_factory=dt.utcnow,
        description="Timestamp when calculation was performed"
    )


class TransitAspectsRequest(BaseModel):
    """Request for calculating transit aspects (current planets aspecting natal planets)."""

    natal_datetime: DateTimeRequest = Field(..., description="Birth date and time")
    natal_location: LocationRequest = Field(..., description="Birth location")
    transit_datetime: Optional[DateTimeRequest] = Field(
        default=None,
        description="Transit date/time (if None, uses current time)"
    )
    transit_location: Optional[LocationRequest] = Field(
        default=None,
        description="Transit location (if None, uses natal location)"
    )
    include_all_bodies: bool = Field(
        default=False,
        description="Whether to include all bodies or just major planets"
    )
    include_minor_aspects: bool = Field(
        default=False,
        description="Whether to include minor aspects"
    )
    custom_orbs: Optional[Dict[str, float]] = Field(
        default=None,
        description="Custom orbs for aspects"
    )


class TransitAspectsResponse(BaseModel):
    """Response containing transit aspects."""

    aspects: List[Aspect]
    total_aspects: int = Field(..., description="Total number of transit aspects found")
    natal_datetime: DateTimeRequest
    natal_location: LocationRequest
    transit_datetime: DateTimeRequest
    transit_location: LocationRequest
    calculated_at: dt = Field(
        default_factory=dt.utcnow,
        description="Timestamp when calculation was performed"
    )


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="API status (ok or error)")
    ephemeris_available: bool = Field(
        ..., description="Whether ephemeris data is available"
    )
    message: Optional[str] = Field(default=None, description="Additional information")
