"""Utilities for time and timezone conversions."""

from datetime import datetime
import pytz
from app.models.schemas import DateTimeRequest
from app.core.exceptions import InvalidDateTimeError


def parse_datetime_with_timezone(dt_request: DateTimeRequest, tz_str: str) -> datetime:
    """
    Create a timezone-aware datetime from request components.

    Args:
        dt_request: DateTimeRequest with year, month, day, hour, minute, second
        tz_str: IANA timezone string

    Returns:
        Timezone-aware datetime object

    Raises:
        InvalidDateTimeError: If datetime is invalid
    """
    try:
        tz = pytz.timezone(tz_str)
        dt = datetime(
            dt_request.year,
            dt_request.month,
            dt_request.day,
            dt_request.hour,
            dt_request.minute,
            dt_request.second,
        )
        # Localize to the specified timezone (handles DST correctly)
        return tz.localize(dt)
    except ValueError as e:
        raise InvalidDateTimeError(f"Invalid datetime: {e}")
    except Exception as e:
        raise InvalidDateTimeError(f"Error parsing datetime: {e}")


def to_utc(dt: datetime) -> datetime:
    """
    Convert a timezone-aware datetime to UTC.

    Args:
        dt: Timezone-aware datetime

    Returns:
        Datetime in UTC timezone
    """
    if dt.tzinfo is None:
        raise InvalidDateTimeError("Datetime must be timezone-aware")
    return dt.astimezone(pytz.UTC)


def validate_timezone(tz_str: str) -> bool:
    """
    Validate a timezone string against the pytz database.

    Args:
        tz_str: IANA timezone string

    Returns:
        True if valid, False otherwise
    """
    try:
        pytz.timezone(tz_str)
        return True
    except pytz.exceptions.UnknownTimeZoneError:
        return False
