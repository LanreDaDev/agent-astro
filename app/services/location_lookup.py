"""Location lookup service for converting place names to coordinates and timezones."""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from timezonefinder import TimezoneFinder
from typing import Dict
from app.core.exceptions import InvalidLocationError


class LocationLookupService:
    """Service for looking up location coordinates and timezone from place names."""

    def __init__(self):
        self.geolocator = Nominatim(user_agent="astrology-api")
        self.tf = TimezoneFinder()

    def lookup_location(self, query: str) -> Dict[str, any]:
        """
        Look up coordinates and timezone for a location.

        Args:
            query: Location name (e.g., "New York", "London, UK", "Tokyo, Japan")

        Returns:
            Dictionary with latitude, longitude, timezone, and full address

        Raises:
            InvalidLocationError: If location cannot be found
        """
        try:
            # Geocode the location
            location = self.geolocator.geocode(query, timeout=10)

            if not location:
                raise InvalidLocationError(f"Location not found: {query}")

            # Get timezone from coordinates
            timezone = self.tf.timezone_at(
                lat=location.latitude, lng=location.longitude
            )

            if not timezone:
                raise InvalidLocationError(
                    f"Could not determine timezone for coordinates: "
                    f"{location.latitude}, {location.longitude}"
                )

            return {
                "address": location.address,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timezone": timezone,
            }

        except GeocoderTimedOut:
            raise InvalidLocationError("Location lookup timed out. Please try again.")
        except GeocoderServiceError as e:
            raise InvalidLocationError(f"Geocoding service error: {e}")
        except Exception as e:
            raise InvalidLocationError(f"Error looking up location: {e}")


# Global instance
location_lookup_service = LocationLookupService()
