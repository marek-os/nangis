# Created by mareko@hi.no at 27.02.2025

# os to tauk gis conversions

from datetime import datetime
from nangis.datex import jdn_to_datetime, datetime_to_jdn

def jdn2dk(jdate : float) -> tuple:
    return datetime2dk(jdn_to_datetime(jdate))

def dk2jdn(dkdate : tuple) -> float:
    return datetime2dk(datetime_to_jdn(dkdate))


def datetime2dk(dt: datetime) -> tuple:
    """Convert a datetime object to TatukGIS date tuple format."""
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    weekday = dt.weekday()  # Monday = 0, Sunday = 6
    yearday = dt.timetuple().tm_yday  # Julian day (1-366)
    dst_flag = -1  # DST information is unknown in TatukGIS

    return (year, month, day, hour, minute, second, weekday, yearday, dst_flag)



def dk2datetime(dk_date: tuple) -> datetime:
    """Convert a TatukGIS date tuple to a Python datetime object.

    Ensures the input has exactly 9 elements.
    """
    if len(dk_date) != 9:
        raise ValueError(f"Invalid TatukGIS date format: Expected 9 elements, got {len(dk_date)}")

    year, month, day, hour, minute, second, _, _, _ = dk_date  # Ignore weekday, yearday, DST flag
    return datetime(year, month, day, hour, minute, second)



if __name__ == '__main__':
    # Example usage
    dt = datetime(2018, 11, 26, 0, 0, 0)  # Example date
    tatukgis_date = datetime2dk(dt)

    print(tatukgis_date)
    # Output: (2018, 11, 26, 0, 0, 0, 0, 330, -1)

    # Example usage
    tatukgis_date = (2018, 11, 26, 0, 0, 0, 0, 330, -1)  # Valid input
    dt = dk2datetime(tatukgis_date)
    print(dt)  # Output: 2018-11-26 00:00:00

    # Invalid input example
    invalid_tatukgis_date = (2018, 11, 26, 0, 0, 0, 0)  # Only 7 elements

    try:
        dt = dk2datetime(invalid_tatukgis_date)
    except ValueError as e:
        print(f"Error: {e}")  # Output: Error: Invalid TatukGIS date format: Expected 9 elements, got 7
