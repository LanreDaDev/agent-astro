"""Tests for planets API endpoints."""

import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "ephemeris_available" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_calculate_planetary_positions(client):
    """Test POST /planets/positions endpoint."""
    request_data = {
        "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
    }

    response = client.post("/api/v1/planets/positions", json=request_data)

    # Should succeed even without ephemeris data (will use built-in Moshier)
    # or return 503 if not available
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "planets" in data
        assert len(data["planets"]) == 10  # All major planets
        assert "calculated_at" in data

        # Check first planet has required fields
        planet = data["planets"][0]
        assert "planet" in planet
        assert "longitude" in planet
        assert "zodiac_sign" in planet
        assert "zodiac_degree" in planet
        assert "retrograde" in planet


def test_get_single_planet_position(client):
    """Test GET /planets/{planet_name}/position endpoint."""
    response = client.get(
        "/api/v1/planets/Sun/position",
        params={
            "year": 2000,
            "month": 1,
            "day": 1,
            "hour": 12,
            "minute": 0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
    )

    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert data["planet"] == "Sun"
        assert "longitude" in data
        assert "zodiac_sign" in data


def test_invalid_planet_name(client):
    """Test invalid planet name returns 404."""
    response = client.get(
        "/api/v1/planets/InvalidPlanet/position",
        params={
            "year": 2000,
            "month": 1,
            "day": 1,
            "hour": 12,
            "minute": 0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
    )

    assert response.status_code == 404


def test_invalid_date(client):
    """Test invalid date returns 400."""
    request_data = {
        "datetime": {
            "year": 2000,
            "month": 2,
            "day": 30,  # February doesn't have 30 days
            "hour": 12,
            "minute": 0,
        },
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
    }

    response = client.post("/api/v1/planets/positions", json=request_data)
    assert response.status_code == 422  # Pydantic validation error


def test_invalid_timezone(client):
    """Test invalid timezone returns 422."""
    request_data = {
        "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "Invalid/Timezone",
        },
    }

    response = client.post("/api/v1/planets/positions", json=request_data)
    assert response.status_code == 422  # Pydantic validation error


def test_invalid_coordinates(client):
    """Test invalid coordinates return 422."""
    request_data = {
        "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
        "location": {
            "latitude": 100,  # Invalid: > 90
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
    }

    response = client.post("/api/v1/planets/positions", json=request_data)
    assert response.status_code == 422  # Pydantic validation error
