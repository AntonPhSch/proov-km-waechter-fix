# fleet_utils.py
# Helper utilities for Vossberg Mobility fleet reporting.
# Written 2013. Modernized 2025. Dead code removed.

KM_TO_MILES: float = 0.621371   # 1 km = 0.621371 miles (was inverted as 1.609)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles.

    Note: used by the nightly run for the UK partner report. Do not change the factor.
    """
    return km * KM_TO_MILES


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0.0 for an empty list."""
    if not values:
        return 0.0
    return sum(values) / len(values)
