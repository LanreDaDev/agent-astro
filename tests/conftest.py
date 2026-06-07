"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import DateTimeRequest, LocationRequest


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_datetime():
    """Sample datetime for testing."""
    return DateTimeRequest(year=2000, month=1, day=1, hour=12, minute=0, second=0)


@pytest.fixture
def sample_location():
    """Sample location for testing (New York City)."""
    return LocationRequest(
        latitude=40.7128, longitude=-74.0060, timezone="America/New_York"
    )


@pytest.fixture
def known_julian_day():
    """
    Known Julian Day for testing.
    2000-01-01 12:00 UTC = JD 2451545.0 (J2000.0 epoch)
    """
    return 2451545.0
