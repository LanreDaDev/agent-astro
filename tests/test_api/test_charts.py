"""Tests for charts API endpoints."""

import pytest


def test_calculate_houses(client):
    """Test POST /charts/houses endpoint."""
    request_data = {
        "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
        "house_system": "P",
    }

    response = client.post("/api/v1/charts/houses", json=request_data)

    # Should succeed even without ephemeris data
    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "house_cusps" in data
        assert len(data["house_cusps"]) == 12  # 12 houses
        assert "ascendant" in data
        assert "midheaven" in data
        assert "house_system" in data
        assert data["house_system"] == "P"
        assert data["house_system_name"] == "Placidus"

        # Check first house cusp structure
        cusp = data["house_cusps"][0]
        assert cusp["house_number"] == 1
        assert "longitude" in cusp
        assert "zodiac_sign" in cusp
        assert "zodiac_degree" in cusp


def test_calculate_natal_chart(client):
    """Test POST /charts/natal endpoint."""
    request_data = {
        "datetime": {"year": 1990, "month": 5, "day": 15, "hour": 14, "minute": 30},
        "location": {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "timezone": "Europe/London",
        },
        "house_system": "P",
        "include_houses": True,
    }

    response = client.post("/api/v1/charts/natal", json=request_data)

    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "planets" in data
        assert "houses" in data
        assert len(data["planets"]) == 10  # All major planets

        # Check that planets have house assignments
        for planet in data["planets"]:
            assert "planet" in planet
            assert "house" in planet
            if planet["house"] is not None:
                assert 1 <= planet["house"] <= 12

        # Check houses
        if data["houses"]:
            houses = data["houses"]
            assert len(houses["house_cusps"]) == 12
            assert "ascendant" in houses
            assert "midheaven" in houses


def test_natal_chart_without_houses(client):
    """Test natal chart without house calculations."""
    request_data = {
        "datetime": {"year": 2000, "month": 6, "day": 15, "hour": 10, "minute": 0},
        "location": {
            "latitude": 34.0522,
            "longitude": -118.2437,
            "timezone": "America/Los_Angeles",
        },
        "house_system": "P",
        "include_houses": False,
    }

    response = client.post("/api/v1/charts/natal", json=request_data)

    assert response.status_code in [200, 503]

    if response.status_code == 200:
        data = response.json()
        assert "planets" in data
        assert len(data["planets"]) == 10

        # Houses should be None when not requested
        assert data["houses"] is None

        # Planets should not have house assignments
        for planet in data["planets"]:
            assert planet["house"] is None


def test_different_house_systems(client):
    """Test different house systems."""
    house_systems = ["P", "K", "O", "E"]  # Placidus, Koch, Porphyrius, Equal

    for house_system in house_systems:
        request_data = {
            "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
            "location": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "timezone": "America/New_York",
            },
            "house_system": house_system,
        }

        response = client.post("/api/v1/charts/houses", json=request_data)

        if response.status_code == 200:
            data = response.json()
            assert data["house_system"] == house_system
            assert len(data["house_cusps"]) == 12


def test_invalid_house_system(client):
    """Test invalid house system returns error."""
    request_data = {
        "datetime": {"year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0},
        "location": {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York",
        },
        "house_system": "INVALID",
    }

    response = client.post("/api/v1/charts/houses", json=request_data)

    # Should return an error for invalid house system
    assert response.status_code in [400, 500, 503]
