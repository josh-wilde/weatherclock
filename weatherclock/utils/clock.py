from numpy import pi

from weatherclock.date_time.date_time import DateTime


def get_hour_angle(dt: DateTime) -> float:
    """Return the hour angle from a datetime object."""
    return (
        2 * pi * dt.hour / 12
        + 2 * pi * dt.minute / (12 * 60)
        + 2 * dt.second / (12 * 60 * 60)
        - pi / 6.0
    )


def get_minute_angle(dt: DateTime) -> float:
    """Return the minute angle from a datetime object."""
    return 2 * pi * dt.minute / 60 + 2 * pi * dt.second / (60 * 60) - pi / 6.0


def get_second_angle(dt: DateTime) -> float:
    """Return the second angle from a datetime object."""
    return 2 * pi * dt.second / 60 - pi / 6.0
