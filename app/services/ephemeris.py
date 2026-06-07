"""Swiss Ephemeris integration service."""

import swisseph as swe
from datetime import datetime
from typing import Dict, Tuple, List, Optional
from app.core.constants import (
    MAJOR_PLANETS,
    NODES,
    ASTEROIDS,
    URANIAN_PLANETS,
    LUNAR_APOGEE,
    ALL_BODIES,
    CALCULATED_POINTS,
    ZODIAC_SIGNS,
    HOUSE_SYSTEMS,
)
from app.core.exceptions import (
    EphemerisDataError,
    CalculationError,
    InvalidPlanetError,
)


class EphemerisService:
    """Service for Swiss Ephemeris calculations."""

    def __init__(self):
        self._initialized = False

    def initialize(self, ephemeris_path: str) -> None:
        """
        Initialize Swiss Ephemeris with data path.

        Args:
            ephemeris_path: Path to directory containing ephemeris data files
        """
        try:
            swe.set_ephe_path(ephemeris_path)
            self._initialized = True
        except Exception as e:
            raise EphemerisDataError(f"Failed to initialize ephemeris: {e}")

    def check_ephemeris_available(self) -> bool:
        """
        Check if ephemeris data is available.

        Returns:
            True if ephemeris can perform calculations
        """
        if not self._initialized:
            return False
        try:
            # Try a simple calculation to verify data is available
            jd = swe.julday(2000, 1, 1, 12.0)
            swe.calc_ut(jd, swe.SUN)
            return True
        except Exception:
            return False

    def datetime_to_julian_day(self, dt: datetime) -> float:
        """
        Convert datetime to Julian Day number.

        Args:
            dt: Datetime object (should be in UTC)

        Returns:
            Julian Day number

        Raises:
            CalculationError: If conversion fails
        """
        try:
            hour = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
            jd = swe.julday(dt.year, dt.month, dt.day, hour)
            return jd
        except Exception as e:
            raise CalculationError(f"Failed to convert datetime to Julian Day: {e}")

    def calculate_planet_position(
        self, julian_day: float, planet_id: int
    ) -> Dict[str, float]:
        """
        Calculate position of a planet at a given Julian Day.

        Args:
            julian_day: Julian Day number
            planet_id: Swiss Ephemeris planet ID

        Returns:
            Dictionary with longitude, latitude, distance, and speed

        Raises:
            CalculationError: If calculation fails
        """
        try:
            # SEFLG_SWIEPH uses Swiss Ephemeris
            # SEFLG_SPEED calculates daily motion
            flags = swe.FLG_SWIEPH | swe.FLG_SPEED
            result = swe.calc_ut(julian_day, planet_id, flags)

            # result is tuple: (positions, return_flag)
            # positions: [longitude, latitude, distance, speed_long, speed_lat, speed_dist]
            positions = result[0]

            return {
                "longitude": positions[0],
                "latitude": positions[1],
                "distance": positions[2],
                "speed": positions[3],  # speed in longitude (daily motion)
            }
        except Exception as e:
            raise CalculationError(f"Failed to calculate planet position: {e}")

    def longitude_to_zodiac(self, longitude: float) -> Tuple[str, float]:
        """
        Convert absolute longitude (0-360) to zodiac sign and degree within sign.

        Args:
            longitude: Absolute ecliptic longitude in degrees (0-360)

        Returns:
            Tuple of (zodiac_sign, degree_within_sign)
        """
        # Normalize longitude to 0-360 range
        longitude = longitude % 360

        # Each zodiac sign spans 30 degrees
        sign_index = int(longitude / 30)
        degree_in_sign = longitude % 30

        zodiac_sign = ZODIAC_SIGNS[sign_index]

        return zodiac_sign, degree_in_sign

    def is_retrograde(self, speed: float) -> bool:
        """
        Determine if a planet is in retrograde motion.

        Args:
            speed: Daily motion in degrees (can be negative)

        Returns:
            True if planet is retrograde (negative speed)
        """
        return speed < 0

    def get_body_id(self, body_name: str) -> Tuple[int, str]:
        """
        Get Swiss Ephemeris body ID and type from body name.

        Args:
            body_name: Name of the celestial body

        Returns:
            Tuple of (body_id, body_type) where body_type is 'planet', 'asteroid', or 'calculated'

        Raises:
            InvalidPlanetError: If body name is not recognized
        """
        # Check if it's a calculated point
        if body_name in CALCULATED_POINTS:
            return (0, "calculated")  # ID doesn't matter for calculated points

        # Check in all body dictionaries
        if body_name in ALL_BODIES:
            body_id = ALL_BODIES[body_name]

            # Determine if it's an asteroid (needs offset)
            if body_name in ASTEROIDS and body_name != "Chiron":
                # Asteroids (except Chiron) need AST_OFFSET added
                return (body_id + swe.AST_OFFSET, "asteroid")
            else:
                return (body_id, "planet")

        raise InvalidPlanetError(
            f"Unknown celestial body: {body_name}. "
            f"Valid bodies: {', '.join(sorted(list(ALL_BODIES.keys()) + CALCULATED_POINTS))}"
        )

    def get_planet_id(self, planet_name: str) -> int:
        """
        Get Swiss Ephemeris planet ID from planet name.

        Deprecated: Use get_body_id() for new code.

        Args:
            planet_name: Name of the planet (e.g., 'Sun', 'Moon', 'Mars')

        Returns:
            Swiss Ephemeris planet ID

        Raises:
            InvalidPlanetError: If planet name is not recognized
        """
        body_id, body_type = self.get_body_id(planet_name)
        return body_id

    def calculate_houses(
        self, julian_day: float, latitude: float, longitude: float, house_system: str = "P"
    ) -> Dict[str, any]:
        """
        Calculate astrological houses for a given time and location.

        Args:
            julian_day: Julian Day number
            latitude: Latitude in degrees (-90 to 90)
            longitude: Longitude in degrees (-180 to 180)
            house_system: House system code (P=Placidus, K=Koch, etc.)

        Returns:
            Dictionary with house cusps, ascendant, midheaven, and other angles

        Raises:
            CalculationError: If house calculation fails
        """
        try:
            # Validate house system
            if house_system not in HOUSE_SYSTEMS:
                raise CalculationError(
                    f"Invalid house system: {house_system}. "
                    f"Valid systems: {', '.join(HOUSE_SYSTEMS.keys())}"
                )

            # Calculate houses
            # swe.houses returns: (cusps, ascmc)
            # cusps: tuple of 12 house cusps (houses 1-12)
            # ascmc: tuple with [Ascendant, MC, ARMC, Vertex, Equatorial Ascendant, Co-Ascendant (Koch), ...]
            result = swe.houses(julian_day, latitude, longitude, house_system.encode('ascii'))
            cusps, ascmc = result

            # Extract house cusps (all 12)
            house_cusps = list(cusps)

            # Extract important angles
            ascendant = ascmc[0]  # Ascendant (1st house cusp)
            midheaven = ascmc[1]  # MC (Midheaven, 10th house cusp)
            armc = ascmc[2]  # Right Ascension of MC
            vertex = ascmc[3]  # Vertex

            return {
                "house_cusps": house_cusps,
                "ascendant": ascendant,
                "midheaven": midheaven,
                "armc": armc,
                "vertex": vertex,
                "house_system": house_system,
            }
        except Exception as e:
            raise CalculationError(f"Failed to calculate houses: {e}")

    def get_planet_house(self, planet_longitude: float, house_cusps: List[float]) -> int:
        """
        Determine which house a planet is in based on its longitude and house cusps.

        Args:
            planet_longitude: Planet's ecliptic longitude (0-360)
            house_cusps: List of 12 house cusp longitudes

        Returns:
            House number (1-12)
        """
        # Normalize planet longitude
        planet_lon = planet_longitude % 360

        # Check each house
        for i in range(12):
            cusp_start = house_cusps[i] % 360
            # Next house cusp (wraps around to house 1)
            cusp_end = house_cusps[(i + 1) % 12] % 360

            # Handle cases where house crosses 0° Aries
            if cusp_start > cusp_end:
                # House crosses 0°
                if planet_lon >= cusp_start or planet_lon < cusp_end:
                    return i + 1
            else:
                # Normal case
                if cusp_start <= planet_lon < cusp_end:
                    return i + 1

        # Fallback (should not happen)
        return 1

    def is_day_chart(self, sun_longitude: float, ascendant: float, sun_house: Optional[int] = None) -> bool:
        """
        Determine if a chart is a day or night chart.

        Day chart: Sun is above the horizon (houses 7-12)
        Night chart: Sun is below the horizon (houses 1-6)

        Args:
            sun_longitude: Sun's ecliptic longitude
            ascendant: Ascendant longitude
            sun_house: Sun's house number (1-12). If provided, uses this for determination (most reliable).

        Returns:
            True if day chart, False if night chart
        """
        # PREFERRED METHOD: Use house position if available
        # Houses 7-12 are above the horizon (Day chart)
        # Houses 1-6 are below the horizon (Night chart)
        if sun_house is not None:
            return 7 <= sun_house <= 12

        # FALLBACK METHOD: Use longitude comparison
        # Only used if house position is not available
        # Normalize to 0-360
        sun_lon = sun_longitude % 360
        asc = ascendant % 360
        desc = (asc + 180.0) % 360

        # Sun is above horizon if it's between Ascendant and Descendant
        # going through the upper hemisphere (through MC)
        if asc < desc:
            # Normal case: ASC at 30°, DESC at 210°
            # Day if Sun is between 30° and 210°
            return asc <= sun_lon <= desc
        else:
            # Wrapped case: ASC at 330°, DESC at 150°
            # Day if Sun is between 330°-360° or 0°-150°
            return sun_lon >= asc or sun_lon <= desc

    def calculate_calculated_point(
        self,
        point_name: str,
        julian_day: float,
        latitude: float,
        longitude: float,
        house_system: str = "P",
    ) -> Optional[float]:
        """
        Calculate special astrological points that are derived from other calculations.

        Args:
            point_name: Name of the calculated point
            julian_day: Julian Day number
            latitude: Latitude in degrees
            longitude: Longitude in degrees
            house_system: House system code

        Returns:
            Longitude of the calculated point in degrees (0-360), or None if cannot calculate

        Raises:
            CalculationError: If calculation fails
        """
        try:
            if point_name == "South Node":
                # South Node is always opposite North Node (Mean Node)
                north_node_pos = self.calculate_planet_position(julian_day, swe.MEAN_NODE)
                return (north_node_pos["longitude"] + 180.0) % 360

            elif point_name == "Descendant":
                # Descendant is opposite Ascendant
                houses = self.calculate_houses(julian_day, latitude, longitude, house_system)
                return (houses["ascendant"] + 180.0) % 360

            elif point_name == "IC":
                # IC is opposite MC (Midheaven)
                houses = self.calculate_houses(julian_day, latitude, longitude, house_system)
                return (houses["midheaven"] + 180.0) % 360

            elif point_name == "Priapus":
                # Priapus is opposite Black Moon Lilith
                lilith_pos = self.calculate_planet_position(julian_day, swe.MEAN_APOG)
                return (lilith_pos["longitude"] + 180.0) % 360

            elif point_name == "Part of Fortune":
                # Part of Fortune formula depends on day/night chart
                # Day chart: Asc + Moon - Sun
                # Night chart: Asc + Sun - Moon
                houses = self.calculate_houses(julian_day, latitude, longitude, house_system)
                sun_pos = self.calculate_planet_position(julian_day, swe.SUN)
                moon_pos = self.calculate_planet_position(julian_day, swe.MOON)

                # Determine Sun's house for day/night chart determination
                sun_house = self.get_planet_house(sun_pos["longitude"], houses["house_cusps"])

                # Determine if day or night chart using Sun's house (most reliable)
                is_day = self.is_day_chart(sun_pos["longitude"], houses["ascendant"], sun_house)

                if is_day:
                    # Day formula: Asc + Moon - Sun
                    pof = houses["ascendant"] + moon_pos["longitude"] - sun_pos["longitude"]
                else:
                    # Night formula: Asc + Sun - Moon
                    pof = houses["ascendant"] + sun_pos["longitude"] - moon_pos["longitude"]

                return pof % 360

            elif point_name == "Part of Spirit":
                # Part of Spirit is the reverse of Part of Fortune
                # Day chart: Asc + Sun - Moon
                # Night chart: Asc + Moon - Sun
                houses = self.calculate_houses(julian_day, latitude, longitude, house_system)
                sun_pos = self.calculate_planet_position(julian_day, swe.SUN)
                moon_pos = self.calculate_planet_position(julian_day, swe.MOON)

                # Determine Sun's house for day/night chart determination
                sun_house = self.get_planet_house(sun_pos["longitude"], houses["house_cusps"])

                # Determine if day or night chart using Sun's house (most reliable)
                is_day = self.is_day_chart(sun_pos["longitude"], houses["ascendant"], sun_house)

                if is_day:
                    # Day formula: Asc + Sun - Moon
                    pos = houses["ascendant"] + sun_pos["longitude"] - moon_pos["longitude"]
                else:
                    # Night formula: Asc + Moon - Sun
                    pos = houses["ascendant"] + moon_pos["longitude"] - sun_pos["longitude"]

                return pos % 360

            else:
                raise CalculationError(f"Unknown calculated point: {point_name}")

        except Exception as e:
            raise CalculationError(f"Failed to calculate {point_name}: {e}")


# Global ephemeris service instance
ephemeris_service = EphemerisService()
