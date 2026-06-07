"""High-level calculator service for astrological calculations."""

from datetime import datetime
from typing import List, Optional
from app.models.schemas import PlanetPosition, HouseCusp, HousesResponse
from app.services.ephemeris import ephemeris_service
from app.core.constants import (
    MAJOR_PLANETS,
    NODES,
    ASTEROIDS,
    URANIAN_PLANETS,
    LUNAR_APOGEE,
    ALL_BODIES,
    CALCULATED_POINTS,
    HOUSE_SYSTEMS,
)
from app.core.exceptions import InvalidPlanetError
from app.utils.time_converter import to_utc


class CalculatorService:
    """Service for high-level astrological calculations."""

    def __init__(self):
        self.ephemeris = ephemeris_service

    def calculate_all_planets(
        self, dt: datetime, lat: float, lon: float, house_cusps: Optional[List[float]] = None
    ) -> List[PlanetPosition]:
        """
        Calculate positions for all major planets (original 10).

        Args:
            dt: Timezone-aware datetime
            lat: Latitude (for house calculations)
            lon: Longitude (for house calculations)
            house_cusps: Optional list of 12 house cusps for house assignment

        Returns:
            List of PlanetPosition objects for all major planets
        """
        # Convert to UTC for calculations
        dt_utc = to_utc(dt)

        # Convert to Julian Day
        julian_day = self.ephemeris.datetime_to_julian_day(dt_utc)

        positions = []
        for planet_name in MAJOR_PLANETS.keys():
            planet_position = self._calculate_body(planet_name, julian_day, house_cusps, lat, lon)
            positions.append(planet_position)

        return positions

    def calculate_all_bodies(
        self, dt: datetime, lat: float, lon: float, house_cusps: Optional[List[float]] = None, house_system: str = "P"
    ) -> List[PlanetPosition]:
        """
        Calculate positions for ALL celestial bodies (planets, asteroids, nodes, calculated points).

        Args:
            dt: Timezone-aware datetime
            lat: Latitude (for house calculations and calculated points)
            lon: Longitude (for house calculations and calculated points)
            house_cusps: Optional list of 12 house cusps for house assignment
            house_system: House system code (needed for calculated points)

        Returns:
            List of PlanetPosition objects for all bodies
        """
        # Convert to UTC for calculations
        dt_utc = to_utc(dt)

        # Convert to Julian Day
        julian_day = self.ephemeris.datetime_to_julian_day(dt_utc)

        positions = []

        # Calculate all regular bodies (planets, nodes, asteroids, uranian planets, lilith)
        for body_name in ALL_BODIES.keys():
            try:
                body_position = self._calculate_body(body_name, julian_day, house_cusps, lat, lon)
                positions.append(body_position)
            except Exception as e:
                # Skip bodies that fail to calculate (usually due to missing ephemeris data)
                # This is expected for asteroids if seas_18.se1 or specific asteroid files aren't available
                import logging
                logging.warning(f"Skipping {body_name}: {str(e)}")
                continue

        # Calculate all calculated points
        for point_name in CALCULATED_POINTS:
            try:
                point_position = self._calculate_calculated_point(
                    point_name, julian_day, lat, lon, house_cusps, house_system
                )
                positions.append(point_position)
            except Exception as e:
                # Skip points that fail to calculate
                import logging
                logging.warning(f"Skipping {point_name}: {str(e)}")
                continue

        return positions

    def calculate_single_planet(
        self, planet_name: str, dt: datetime, lat: float, lon: float, house_cusps: Optional[List[float]] = None
    ) -> PlanetPosition:
        """
        Calculate position for a single planet.

        Args:
            planet_name: Name of the planet
            dt: Timezone-aware datetime
            lat: Latitude (for house calculations)
            lon: Longitude (for house calculations)
            house_cusps: Optional list of 12 house cusps for house assignment

        Returns:
            PlanetPosition object

        Raises:
            InvalidPlanetError: If planet name is invalid
        """
        # Convert to UTC for calculations
        dt_utc = to_utc(dt)

        # Convert to Julian Day
        julian_day = self.ephemeris.datetime_to_julian_day(dt_utc)

        return self._calculate_body(planet_name, julian_day, house_cusps, lat, lon)

    def _calculate_planet(self, planet_name: str, julian_day: float, house_cusps: Optional[List[float]] = None) -> PlanetPosition:
        """
        Internal method to calculate planet position (deprecated, use _calculate_body).

        Args:
            planet_name: Name of the planet
            julian_day: Julian Day number
            house_cusps: Optional list of house cusps for house assignment

        Returns:
            PlanetPosition object
        """
        return self._calculate_body(planet_name, julian_day, house_cusps, 0, 0)

    def _calculate_body(
        self, body_name: str, julian_day: float, house_cusps: Optional[List[float]], lat: float, lon: float
    ) -> PlanetPosition:
        """
        Internal method to calculate celestial body position.

        Args:
            body_name: Name of the celestial body
            julian_day: Julian Day number
            house_cusps: Optional list of house cusps for house assignment
            lat: Latitude (for calculated points)
            lon: Longitude (for calculated points)

        Returns:
            PlanetPosition object
        """
        # Get body ID and type
        body_id, body_type = self.ephemeris.get_body_id(body_name)

        # Calculate position
        position = self.ephemeris.calculate_planet_position(julian_day, body_id)

        # Convert longitude to zodiac sign and degree
        zodiac_sign, zodiac_degree = self.ephemeris.longitude_to_zodiac(
            position["longitude"]
        )

        # Check if retrograde
        is_retrograde = self.ephemeris.is_retrograde(position["speed"])

        # Determine house if cusps are provided
        house_number = None
        if house_cusps:
            house_number = self.ephemeris.get_planet_house(position["longitude"], house_cusps)

        return PlanetPosition(
            planet=body_name,
            longitude=position["longitude"],
            latitude=position["latitude"],
            distance=position["distance"],
            speed=position["speed"],
            zodiac_sign=zodiac_sign,
            zodiac_degree=zodiac_degree,
            retrograde=is_retrograde,
            house=house_number,
        )

    def _calculate_calculated_point(
        self,
        point_name: str,
        julian_day: float,
        lat: float,
        lon: float,
        house_cusps: Optional[List[float]],
        house_system: str = "P",
    ) -> PlanetPosition:
        """
        Internal method to calculate special calculated points.

        Args:
            point_name: Name of the calculated point
            julian_day: Julian Day number
            lat: Latitude
            lon: Longitude
            house_cusps: Optional list of house cusps
            house_system: House system code

        Returns:
            PlanetPosition object
        """
        # Calculate the point longitude
        point_longitude = self.ephemeris.calculate_calculated_point(
            point_name, julian_day, lat, lon, house_system
        )

        if point_longitude is None:
            raise InvalidPlanetError(f"Could not calculate {point_name}")

        # Convert to zodiac sign and degree
        zodiac_sign, zodiac_degree = self.ephemeris.longitude_to_zodiac(point_longitude)

        # Determine house if cusps are provided
        house_number = None
        if house_cusps:
            house_number = self.ephemeris.get_planet_house(point_longitude, house_cusps)

        # Calculated points don't have latitude, distance, or speed
        return PlanetPosition(
            planet=point_name,
            longitude=point_longitude,
            latitude=0.0,
            distance=0.0,
            speed=0.0,
            zodiac_sign=zodiac_sign,
            zodiac_degree=zodiac_degree,
            retrograde=False,  # Calculated points are not retrograde
            house=house_number,
        )

    def calculate_houses(
        self, dt: datetime, lat: float, lon: float, house_system: str = "P"
    ) -> dict:
        """
        Calculate astrological houses.

        Args:
            dt: Timezone-aware datetime
            lat: Latitude in degrees
            lon: Longitude in degrees
            house_system: House system code (P=Placidus, K=Koch, etc.)

        Returns:
            Dictionary with house information
        """
        # Convert to UTC for calculations
        dt_utc = to_utc(dt)

        # Convert to Julian Day
        julian_day = self.ephemeris.datetime_to_julian_day(dt_utc)

        # Calculate houses
        houses_data = self.ephemeris.calculate_houses(julian_day, lat, lon, house_system)

        return houses_data

    def calculate_natal_chart(
        self, dt: datetime, lat: float, lon: float, house_system: str = "P", include_houses: bool = True, include_all_bodies: bool = False
    ) -> dict:
        """
        Calculate a complete natal chart with planets and houses.

        Args:
            dt: Timezone-aware datetime
            lat: Latitude in degrees
            lon: Longitude in degrees
            house_system: House system code
            include_houses: Whether to include house calculations
            include_all_bodies: Whether to include all bodies (asteroids, nodes, calculated points)

        Returns:
            Dictionary with planets and houses
        """
        # Convert to UTC for calculations
        dt_utc = to_utc(dt)

        # Convert to Julian Day
        julian_day = self.ephemeris.datetime_to_julian_day(dt_utc)

        houses_data = None
        house_cusps = None

        # Calculate houses if requested
        if include_houses:
            houses_data = self.ephemeris.calculate_houses(julian_day, lat, lon, house_system)
            house_cusps = houses_data["house_cusps"]

        # Calculate bodies with house assignments
        if include_all_bodies:
            # Calculate ALL bodies (planets, asteroids, nodes, calculated points)
            planets = self.calculate_all_bodies(dt, lat, lon, house_cusps, house_system)
        else:
            # Calculate only major planets (original 10)
            planets = []
            for planet_name in MAJOR_PLANETS.keys():
                planet_position = self._calculate_body(planet_name, julian_day, house_cusps, lat, lon)
                planets.append(planet_position)

        return {
            "planets": planets,
            "houses": houses_data,
        }


# Global calculator service instance
calculator_service = CalculatorService()
