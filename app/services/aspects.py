"""Aspect calculation service for astrological aspects between planets."""

from typing import List, Dict, Optional
from app.core.constants import ASPECT_TYPES, DEFAULT_ORBS, MAJOR_ASPECTS, MINOR_ASPECTS


class AspectService:
    """Service for calculating astrological aspects between celestial bodies."""

    def __init__(self):
        self.aspect_types = ASPECT_TYPES
        self.default_orbs = DEFAULT_ORBS

    def calculate_aspect_angle(self, longitude1: float, longitude2: float) -> float:
        """
        Calculate the shortest angular distance between two longitudes.

        Args:
            longitude1: First longitude (0-360)
            longitude2: Second longitude (0-360)

        Returns:
            Shortest angular distance (0-180 degrees)
        """
        # Normalize both longitudes to 0-360
        lon1 = longitude1 % 360
        lon2 = longitude2 % 360

        # Calculate the difference
        diff = abs(lon2 - lon1)

        # Take the shorter arc around the circle
        if diff > 180:
            diff = 360 - diff

        return diff

    def is_applying(
        self,
        longitude1: float,
        speed1: float,
        longitude2: float,
        speed2: float,
        aspect_angle: float
    ) -> bool:
        """
        Determine if an aspect is applying (getting tighter) or separating (getting wider).

        Args:
            longitude1: Longitude of first planet
            speed1: Daily motion of first planet (degrees/day)
            longitude2: Longitude of second planet (fixed for transits)
            speed2: Daily motion of second planet (0 for natal planets in transits)
            aspect_angle: The exact angle of the aspect (0, 60, 90, 120, 180, etc.)

        Returns:
            True if applying (aspect getting tighter), False if separating
        """
        # Calculate relative speed (how fast the aspect angle is changing)
        relative_speed = speed1 - speed2

        # If relative speed is 0, aspect is neither applying nor separating (stationary)
        if abs(relative_speed) < 0.001:
            return False

        # Calculate current angular distance
        current_distance = self.calculate_aspect_angle(longitude1, longitude2)

        # Predict where planet1 will be in 1 day
        future_lon1 = (longitude1 + speed1) % 360
        future_distance = self.calculate_aspect_angle(future_lon1, longitude2)

        # Calculate how close to the exact aspect angle
        current_deviation = abs(current_distance - aspect_angle)
        future_deviation = abs(future_distance - aspect_angle)

        # If future deviation is smaller, aspect is applying (getting tighter)
        # If future deviation is larger, aspect is separating (getting wider)
        return future_deviation < current_deviation

    def is_aspect(
        self,
        angle: float,
        aspect_type: str,
        orb: Optional[float] = None
    ) -> tuple[bool, float]:
        """
        Check if an angle forms a specific aspect type.

        Args:
            angle: Angular distance between two points
            aspect_type: Type of aspect to check (e.g., 'conjunction', 'trine')
            orb: Maximum orb (deviation) allowed. If None, uses default orb.

        Returns:
            Tuple of (is_aspect, exact_orb) where exact_orb is the deviation from exact
        """
        if aspect_type not in self.aspect_types:
            return (False, 0.0)

        target_angle = self.aspect_types[aspect_type]
        if orb is None:
            orb = self.default_orbs.get(aspect_type, 8.0)

        # Calculate how far from exact the aspect is
        deviation = abs(angle - target_angle)

        # Check if within orb
        is_valid = deviation <= orb

        return (is_valid, deviation)

    def find_aspect(
        self,
        longitude1: float,
        longitude2: float,
        custom_orbs: Optional[Dict[str, float]] = None,
        include_minor: bool = False
    ) -> Optional[Dict]:
        """
        Find what aspect (if any) exists between two longitudes.

        Args:
            longitude1: First longitude
            longitude2: Second longitude
            custom_orbs: Optional custom orbs to override defaults
            include_minor: Whether to check minor aspects (default: False, major only)

        Returns:
            Dictionary with aspect info, or None if no aspect found
        """
        angle = self.calculate_aspect_angle(longitude1, longitude2)

        # Determine which aspects to check
        if include_minor:
            aspects_to_check = self.aspect_types  # All aspects
        else:
            aspects_to_check = MAJOR_ASPECTS  # Major only

        # Check each aspect type
        orbs = custom_orbs if custom_orbs else self.default_orbs

        for aspect_name, target_angle in aspects_to_check.items():
            orb = orbs.get(aspect_name, 8.0)
            is_valid, deviation = self.is_aspect(angle, aspect_name, orb)

            if is_valid:
                return {
                    "aspect": aspect_name,
                    "angle": target_angle,
                    "orb": deviation,
                    "applying": None,  # Would need speed calculation to determine
                }

        return None

    def calculate_all_aspects(
        self,
        planets: List[Dict],
        custom_orbs: Optional[Dict[str, float]] = None,
        include_same_planet: bool = False,
        include_minor: bool = False
    ) -> List[Dict]:
        """
        Calculate all aspects between a list of planets.

        Args:
            planets: List of planet dictionaries with 'planet' and 'longitude' keys
            custom_orbs: Optional custom orbs
            include_same_planet: Whether to include aspects of a planet to itself (usually False)
            include_minor: Whether to include minor aspects (default: False, major only)

        Returns:
            List of aspect dictionaries
        """
        aspects = []

        # Compare each planet to every other planet
        for i, planet1 in enumerate(planets):
            for planet2 in planets[i + 1:]:  # Only check each pair once
                # Skip if same planet (unless explicitly included)
                if not include_same_planet and planet1["planet"] == planet2["planet"]:
                    continue

                # Find aspect
                aspect = self.find_aspect(
                    planet1["longitude"],
                    planet2["longitude"],
                    custom_orbs,
                    include_minor
                )

                if aspect:
                    aspects.append({
                        "planet1": planet1["planet"],
                        "planet2": planet2["planet"],
                        "aspect": aspect["aspect"],
                        "angle": aspect["angle"],
                        "orb": round(aspect["orb"], 2),
                        "planet1_longitude": round(planet1["longitude"], 2),
                        "planet2_longitude": round(planet2["longitude"], 2),
                    })

        return aspects

    def get_planet_aspects(
        self,
        target_planet: str,
        planets: List[Dict],
        custom_orbs: Optional[Dict[str, float]] = None,
        include_minor: bool = False
    ) -> List[Dict]:
        """
        Get all aspects involving a specific planet.

        Args:
            target_planet: Name of the planet to find aspects for
            planets: List of all planets
            custom_orbs: Optional custom orbs
            include_minor: Whether to include minor aspects

        Returns:
            List of aspects involving the target planet
        """
        all_aspects = self.calculate_all_aspects(planets, custom_orbs, include_minor=include_minor)

        # Filter to only aspects involving the target planet
        planet_aspects = [
            aspect for aspect in all_aspects
            if aspect["planet1"] == target_planet or aspect["planet2"] == target_planet
        ]

        return planet_aspects

    def calculate_transit_aspects(
        self,
        natal_planets: List[Dict],
        transit_planets: List[Dict],
        custom_orbs: Optional[Dict[str, float]] = None,
        include_minor: bool = False
    ) -> List[Dict]:
        """
        Calculate transit aspects (transiting planets aspecting natal planets).

        This is different from calculate_all_aspects because we only compare
        transiting planets TO natal planets (not transits to transits, not natals to natals).

        Args:
            natal_planets: List of natal planet dictionaries
            transit_planets: List of transiting planet dictionaries
            custom_orbs: Optional custom orbs
            include_minor: Whether to include minor aspects

        Returns:
            List of transit aspect dictionaries
        """
        aspects = []

        # Compare each transiting planet to each natal planet
        for transit_planet in transit_planets:
            for natal_planet in natal_planets:
                # Find aspect
                aspect = self.find_aspect(
                    transit_planet["longitude"],
                    natal_planet["longitude"],
                    custom_orbs,
                    include_minor
                )

                if aspect:
                    # Determine if applying or separating
                    # Transit planet has speed, natal planet is fixed (speed=0)
                    applying = None
                    if "speed" in transit_planet:
                        applying = self.is_applying(
                            transit_planet["longitude"],
                            transit_planet["speed"],
                            natal_planet["longitude"],
                            0.0,  # Natal planets don't move
                            aspect["angle"]
                        )

                    aspects.append({
                        "planet1": f"{transit_planet['planet']} (Transit)",
                        "planet2": f"{natal_planet['planet']} (Natal)",
                        "aspect": aspect["aspect"],
                        "angle": aspect["angle"],
                        "orb": round(aspect["orb"], 2),
                        "planet1_longitude": round(transit_planet["longitude"], 2),
                        "planet2_longitude": round(natal_planet["longitude"], 2),
                        "applying": applying,
                        "planet1_retrograde": transit_planet.get("retrograde", None),
                        "planet2_retrograde": natal_planet.get("retrograde", None),
                    })

        return aspects


# Global aspect service instance
aspect_service = AspectService()
