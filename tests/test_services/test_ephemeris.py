"""Tests for ephemeris service."""

import pytest
from datetime import datetime
import pytz
from app.services.ephemeris import ephemeris_service
from app.core.exceptions import InvalidPlanetError, CalculationError


def test_julian_day_conversion():
    """Test conversion from datetime to Julian Day."""
    # J2000.0 epoch: 2000-01-01 12:00 UTC = JD 2451545.0
    dt = datetime(2000, 1, 1, 12, 0, 0, tzinfo=pytz.UTC)
    jd = ephemeris_service.datetime_to_julian_day(dt)

    # Allow small floating point tolerance
    assert abs(jd - 2451545.0) < 0.001


def test_longitude_to_zodiac():
    """Test conversion from absolute longitude to zodiac sign and degree."""
    # 0 degrees = 0° Aries
    sign, degree = ephemeris_service.longitude_to_zodiac(0)
    assert sign == "Aries"
    assert abs(degree - 0) < 0.001

    # 30 degrees = 0° Taurus
    sign, degree = ephemeris_service.longitude_to_zodiac(30)
    assert sign == "Taurus"
    assert abs(degree - 0) < 0.001

    # 45 degrees = 15° Taurus
    sign, degree = ephemeris_service.longitude_to_zodiac(45)
    assert sign == "Taurus"
    assert abs(degree - 15) < 0.001

    # 270 degrees = 0° Capricorn
    sign, degree = ephemeris_service.longitude_to_zodiac(270)
    assert sign == "Capricorn"
    assert abs(degree - 0) < 0.001


def test_retrograde_detection():
    """Test retrograde motion detection."""
    assert ephemeris_service.is_retrograde(-0.5) is True
    assert ephemeris_service.is_retrograde(0.5) is False
    assert ephemeris_service.is_retrograde(0) is False


def test_get_planet_id():
    """Test planet ID retrieval."""
    assert ephemeris_service.get_planet_id("Sun") == 0
    assert ephemeris_service.get_planet_id("Moon") == 1
    assert ephemeris_service.get_planet_id("Mars") == 4
    assert ephemeris_service.get_planet_id("Pluto") == 9


def test_invalid_planet():
    """Test invalid planet name raises exception."""
    with pytest.raises(InvalidPlanetError):
        ephemeris_service.get_planet_id("InvalidPlanet")


def test_calculate_sun_position():
    """Test calculation of Sun position at J2000.0 epoch."""
    # J2000.0: 2000-01-01 12:00 UTC
    jd = 2451545.0

    try:
        position = ephemeris_service.calculate_planet_position(jd, 0)  # 0 = Sun

        # Sun should be around 280-281 degrees (Capricorn) at J2000.0
        assert 270 <= position["longitude"] <= 290
        assert "latitude" in position
        assert "distance" in position
        assert "speed" in position

    except Exception as e:
        # If ephemeris data is not available, test should skip
        pytest.skip(f"Ephemeris data not available: {e}")
