# Created by mareko@hi.no at 27.02.2025

# date time conversions

from datetime import datetime, timedelta

def jdn_to_datetime(jd: float) -> datetime:
    """Convert a Julian Date (JD) to a Python datetime object."""
    julian_epoch = datetime(2000, 1, 1, 12)  # J2000 reference (JD 2451545.0)
    days_since_epoch = jd - 2451545.0  # Days since January 1, 2000, at 12:00 UTC
    return julian_epoch + timedelta(days=days_since_epoch)


def datetime_to_jdn(dt: datetime) -> float:
    """Convert a Python datetime object to Julian Date (JD)."""
    julian_epoch = datetime(2000, 1, 1, 12)  # J2000 reference (JD 2451545.0)
    delta = dt - julian_epoch  # Difference in days
    return 2451545.0 + delta.total_seconds() / 86400  # Convert seconds to days



if __name__ == '__main__':
    # Example usage
    julian_date = 2451545.0  # January 1, 2000, at noon UTC
    gregorian_date = jdn_to_datetime(julian_date)

    print(gregorian_date)  # Output: 2000-01-01 12:00:00


    dt = datetime(2000, 1, 1, 12)  # January 1, 2000, at noon UTC
    jd = datetime_to_jdn(dt)

    print(jd)  # Output: 2451545.0
