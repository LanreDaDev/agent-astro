"""Tests for location lookup endpoint."""

import pytest


def test_lookup_new_york(client):
    """Test location lookup for New York."""
    response = client.get("/api/v1/location/lookup?query=New York, NY")

    assert response.status_code == 200
    data = response.json()

    assert "address" in data
    assert "latitude" in data
    assert "longitude" in data
    assert "timezone" in data

    # Check coordinates are roughly correct for New York
    assert 40.0 < data["latitude"] < 41.0
    assert -75.0 < data["longitude"] < -73.0
    assert data["timezone"] == "America/New_York"


def test_lookup_london(client):
    """Test location lookup for London."""
    response = client.get("/api/v1/location/lookup?query=London, UK")

    assert response.status_code == 200
    data = response.json()

    # Check coordinates are roughly correct for London
    assert 51.0 < data["latitude"] < 52.0
    assert -1.0 < data["longitude"] < 0.5
    assert data["timezone"] == "Europe/London"


def test_lookup_tokyo(client):
    """Test location lookup for Tokyo."""
    response = client.get("/api/v1/location/lookup?query=Tokyo, Japan")

    assert response.status_code == 200
    data = response.json()

    # Check coordinates are roughly correct for Tokyo
    assert 35.0 < data["latitude"] < 36.0
    assert 139.0 < data["longitude"] < 140.0
    assert data["timezone"] == "Asia/Tokyo"


def test_lookup_paris(client):
    """Test location lookup for Paris."""
    response = client.get("/api/v1/location/lookup?query=Paris, France")

    assert response.status_code == 200
    data = response.json()

    # Check coordinates are roughly correct for Paris
    assert 48.0 < data["latitude"] < 49.0
    assert 2.0 < data["longitude"] < 3.0
    assert data["timezone"] == "Europe/Paris"


def test_lookup_invalid_location(client):
    """Test location lookup with invalid location."""
    response = client.get("/api/v1/location/lookup?query=ZZZZZ12345INVALID")

    # Should return 404 for location not found
    assert response.status_code == 404


def test_lookup_empty_query(client):
    """Test location lookup with empty query."""
    response = client.get("/api/v1/location/lookup?query=")

    # Should return 422 validation error (query too short)
    assert response.status_code == 422


def test_lookup_single_word(client):
    """Test location lookup with single word (city name)."""
    response = client.get("/api/v1/location/lookup?query=Berlin")

    assert response.status_code == 200
    data = response.json()

    assert "Berlin" in data["address"]
    assert data["timezone"] == "Europe/Berlin"
