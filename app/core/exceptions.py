"""Custom exceptions for the astrology API."""


class AstrologyAPIException(Exception):
    """Base exception for all astrology API errors."""
    pass


class InvalidDateTimeError(AstrologyAPIException):
    """Raised when an invalid date or time is provided."""
    pass


class InvalidLocationError(AstrologyAPIException):
    """Raised when invalid geographical coordinates are provided."""
    pass


class EphemerisDataError(AstrologyAPIException):
    """Raised when ephemeris data files are missing or corrupted."""
    pass


class CalculationError(AstrologyAPIException):
    """Raised when an error occurs during astrological calculations."""
    pass


class InvalidPlanetError(AstrologyAPIException):
    """Raised when an invalid planet name is provided."""
    pass
