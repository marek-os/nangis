#from tatukgis_pdk import TGIS_LayerVector, TGIS_ShapePoint
import tatukgis_pdk as pdk
from typing import Union, Optional, List
import os
from datetime import datetime, timedelta
import math
import numpy as np
#from tatukgis_pdk import TGIS_FieldType


def has_field(layer: pdk.TGIS_LayerVector, field_name: str) -> bool:
    """
    Checks if a field exists in a TatukGIS vector layer.

    Parameters:
    - layer (pdk.TGIS_LayerVector): The vector layer to check.
    - field_name (str): The name of the field to search for.

    Returns:
    - bool: True if the field exists, False otherwise.
    """
    for i in range(layer.Fields.Count):
        if layer.Fields[i].Name == field_name:
            return True  # ✅ Field found

    return False

def has_fields(layer: pdk.TGIS_LayerVector, field_names: List[str]) -> bool:
    for fl in field_names:
        if not has_field(layer, fl):
            return False
    return True


def get_column_minmax(layer: pdk.TGIS_LayerVector, field_name: str) -> list:
    """
    Computes the minimum and maximum values for a numeric field in a TatukGIS layer.

    Parameters:
    - layer (pdk.TGIS_LayerVector): The vector layer to process.
    - field_name (str): The name of the numeric field.

    Returns:
    - list: A list containing [min_value, max_value].

    Raises:
    - RuntimeError: If the field is not found or is not numeric.
    """

    # Get field index
    field_index = get_field_index(layer, field_name)

    if field_index < 0:
        raise ValueError("[get_column_minmax] ARG2: field not found")

    field_info = layer.Fields[field_index]

    # Validate that the field is numeric
    if field_info.FieldType not in [pdk.TGIS_FieldType().Float, pdk.TGIS_FieldType().Number]:
        raise RuntimeError("[get_column_minmax] ARG2: attempt to compute range of non-numeric field")

    # Initialize min/max values
    min_value = float("inf")
    max_value = float("-inf")

    # Use TatukGIS Enumerator to loop through shapes


    for shape in layer.Loop():
        field_value = shape.GetField(field_name)  # Retrieve field value
        value = float(field_value)  # Convert to float

        # Update min/max
        if value < min_value:
            min_value = value
        if value > max_value:
            max_value = value


    return [min_value, max_value]


def get_field_index(layer: pdk.TGIS_LayerVector, field_name: str) -> int:
    """
    Returns the index of a field in a TatukGIS layer.

    Parameters:
    - layer (pdk.TGIS_LayerVector): The vector layer to search.
    - field_name (str): The name of the field.

    Returns:
    - int: The index of the field, or -1 if not found.
    """
    for i in range(layer.Fields.Count):
        if layer.Fields[i].Name == field_name:
            return i  # Fields are numbered from 0 in Python
    return -1  # Return -1 if not found




def has_any_shapes(layer: pdk.TGIS_LayerVector) -> bool:

    #enum = layer.loop.GetEnumerator()
    if layer.Loop() is None:
        return False
    enum = layer.Loop()
    if enum is None:
        return False
    shp = enum.GetCurrent()
    if shp is None:
            return False
    else:
        return True

def get_field_names(layer: pdk.TGIS_LayerVector, numeric_only: bool =False, use_gis: bool = False) -> Optional[List[str]]:
    if not use_gis:
        gis_fields = {'UID', 'GIS_SRCID', 'GIS_SRC_X', 'GIS_SRC_Y',
                      'UID_', 'UID_01', 'UID_0101', 'UID_010101'}
    else:
        gis_fields = set()

    if layer.Fields.Count == 0:
        return None

    fields = []
    for fif in layer.Fields:

        fld = fif.Name
        ok = True

        if not use_gis and fld in gis_fields:
            ok = False

        if numeric_only and fif.FieldType not in {pdk.TGIS_FieldType().Float, pdk.TGIS_FieldType().Number}:
            ok = False

        if ok:
            fields.append(fld)

    return fields if fields else None


def get_shape_by_column_value(layer : pdk.TGIS_LayerVector
                              , column_name : str
                              , value
                              ) ->pdk.TGIS_Shape:
    """
     retrieves a shape that hold specific value for a specific column
    :param layer: partent layer
    :param column_name: column to search
    :param value: value in that column
    :return: shape object or None
    """
    for shp in layer.Loop():
        if shp.GetField(column_name) == value:
            return shp
    return None


def set_layer(igis: Union[pdk.TGIS_Viewer, pdk.TGIS_ViewerWnd], layer: pdk.TGIS_Layer):

   oldLayer = igis.Get(layer.Name)

   if not oldLayer is None:
            igis.Delete(layer.Name);
   igis.Add(layer)



def jul_to_date_field(julian_date):
    """
    Converts a Julian date to a TGIS_FieldType.Date object.

    Args:
        julian_date (float): The Julian date to convert.

    Returns:
        TGIS_FieldType.Date: The corresponding date.
    """
    yyyy, mm, dd, hh, min, ss = jd_to_calendar(julian_date)
    return calendar_to_tdatetime(yyyy, mm, dd, hh, min, ss)



def jd_to_calendar(jd):
    """
    Converts a Julian Date to a Gregorian calendar date and time.
    @deprecated use julian to date time instead
    Args:
        jd (float): The Julian Date to convert.

    Returns:
        tuple: A tuple containing the year, month, day, hour, minute, and second.
    """
    # Calculate the integer part and the fractional part of the Julian Date
    ijd = int(math.floor(jd + 0.5))
    fjd = jd - ijd + 0.5

    # Convert fractional day to hours, minutes, and seconds
    hours = fjd * 24
    minutes = (hours - int(hours)) * 60
    seconds = (minutes - int(minutes)) * 60

    # Calculate the Gregorian date
    a = ijd + 32044
    b = math.floor((4 * a + 3) / 146097)
    c = a - math.floor((b * 146097) / 4)
    d = math.floor((4 * c + 3) / 1461)
    e = c - math.floor((1461 * d) / 4)
    m = math.floor((5 * e + 2) / 153)

    day = int(e - math.floor((153 * m + 2) / 5) + 1)
    month = int(m + 3 - 12 * math.floor(m / 10))
    year = int(b * 100 + d - 4800 + math.floor(m / 10))

    # Return the date and time components
    return year, month, day, int(hours), int(minutes), int(seconds)

# # Example usage:
# jd = 2451545.0  # Example Julian Date
# gregorian_date = jd_to_gregorian(jd)
# print(f"Gregorian Date and Time: {gregorian_date[0]}-{gregorian_date[1]:02d}-{gregorian_date[2]:02d} "
#       f"{gregorian_date[3]:02d}:{gregorian_date[4]:02d}:{gregorian_date[5]:02d}")

def calendar_to_tdatetime(year, month, day, hour=0, minute=0, second=0):
    """
    Converts a Gregorian date and time to Delphi's TDateTime format.

    Args:
        year (int): Year of the date.
        month (int): Month of the date.
        day (int): Day of the date.
        hour (int): Hour of the time (default is 0).
        minute (int): Minute of the time (default is 0).
        second (int): Second of the time (default is 0).

    Returns:
        float: Corresponding TDateTime value.
    """
    # Base date: December 30, 1899
    base_year = 1899
    base_month = 12
    base_day = 30

    # Calculate the number of days from the base date to the target date
    def days_since_base(y, m, d):
        # Adjust months and years to fit the algorithm
        if m <= 2:
            y -= 1
            m += 12
        # Julian Day Number calculation
        A = y // 100
        B = 2 - A + (A // 4)
        jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5
        return jd

    # Julian Day Number for base and target dates
    jd_base = days_since_base(base_year, base_month, base_day)
    jd_target = days_since_base(year, month, day)

    # Total days difference
    total_days = jd_target - jd_base

    # Fractional day calculation
    fractional_day = (hour / 24) + (minute / 1440) + (second / 86400)

    # TDateTime value
    tdatetime = total_days + fractional_day

    return tdatetime

def julian_to_tdatetime(jd):
    """
    Converts a Julian Date to Delphi TDateTime.

    Args:
        jd (float): Julian Date.

    Returns:
        float: Equivalent TDateTime value.
    """
    return jd - 2415018.5

def tdatetime_to_julian(tdatetime):
    """
    Converts Delphi TDateTime to Julian Date.

    Args:
        tdatetime (float): Delphi TDateTime.

    Returns:
        float: Equivalent Julian Date.
    """
    return tdatetime + 2415018.5


from tatukgis_pdk import TGIS_FieldType

def datetime64_to_tdatetime(dt):
    """
    Converts a numpy.datetime64 to Delphi TDateTime.

    Args:
        dt (numpy.datetime64): DateTime in numpy format.

    Returns:
        float: Equivalent Delphi TDateTime.
    """
    delphi_epoch = np.datetime64("1899-12-30", "D")
    return (dt.astype("datetime64[D]") - delphi_epoch).astype(float)

def tdatetime_to_datetime64(tdatetime):
    """
    Converts Delphi TDateTime to numpy.datetime64.

    Args:
        tdatetime (float): Delphi TDateTime value.

    Returns:
        numpy.datetime64: Equivalent numpy datetime64.
    """
    delphi_epoch = np.datetime64("1899-12-30", "D")
    return delphi_epoch + np.timedelta64(int(tdatetime), "D")

def tdatetime_to_datetime64_full(tdatetime):
    """
    Converts Delphi TDateTime (floating point) to numpy.datetime64 including time.

    Args:
        tdatetime (float): Delphi TDateTime value.

    Returns:
        numpy.datetime64: Equivalent numpy datetime64 including time.
    """
    delphi_epoch = np.datetime64("1899-12-30T00:00:00", "s")  # Delphi zero date (full precision)

    # Convert entire TDateTime value (days + fractional days) to seconds
    seconds_since_delphi = round(tdatetime * 86400)  # Convert days to seconds
    return delphi_epoch + np.timedelta64(seconds_since_delphi, "s")


def tdatetime_to_np(dt):
    """
    Converts Delphi TDateTime (float) from a shapefile to numpy.datetime64.

    Args:
        dt (float): Delphi TDateTime value (days since 1899-12-30).

    Returns:
        numpy.datetime64: Converted date.
    """
    delphi_epoch = np.datetime64("1899-12-30", "D")  # Delphi's zero date
    return delphi_epoch + np.timedelta64(int(dt), "D")

def get_column_names(layer, numeric_only: bool=False, use_gis: bool=False):
    return get_field_names(layer, numeric_only=numeric_only, use_gis=use_gis)

import numpy as np

def get_geometry2(shp : pdk.TGIS_Shape, ipart: int) -> np.ndarray:
    """
    Extracts geometry from a shape part and returns a 2D NumPy array with X and Y coordinates.

    Parameters:
    - shp: The shape object with geometry dataaa.
    - ipart (int): The index of the part to extract.

    Returns:
    - np.ndarray: A (2, N) NumPy array with X and Y coordinates.
    """

    if ipart >= shp.GetNumParts() or ipart < 0:
        raise ValueError(f"DkShapeUtils.getGeometry: ARG2: index={ipart} out of range [0 : {shp.GetNumParts()}]")

    N = shp.GetPartSize(ipart)
    result = np.zeros((2, N), dtype=np.float64)  # ✅ NumPy replacement for Mx.new_double(2, N)

    for i in range(N):
        pt = shp.GetPoint(ipart, i)
        result[0, i] = pt.X  # ✅ Access X coordinate
        result[1, i] = pt.Y  # ✅ Access Y coordinate

    return result


def get_geometry(shp : pdk.TGIS_Shape, ipart: int) -> np.ndarray:
    """
    Extracts geometry from a shape part and returns a 2D NumPy array with X and Y coordinates.

    Parameters:
    - shp: The shape object with geometry dataaa.
    - ipart (int): The index of the part to extract.

    Returns:
    - np.ndarray: A (2, N) NumPy array with X and Y coordinates.
    """

    if ipart >= shp.GetNumParts() or ipart < 0:
        raise ValueError(f"DkShapeUtils.getGeometry: ARG2: index={ipart} out of range [0 : {shp.GetNumParts()}]")

    N = shp.GetPartSize(ipart)
    result = np.zeros(2 * N, dtype=np.float64)  # ✅ Correct shape (1D array)

    for i in range(N):
        pt = shp.GetPoint(ipart, i)
        result[2 * i] = pt.X  # ✅ Store Longitude at even indices
        result[2 * i + 1] = pt.Y  # ✅ Store Latitude at odd indices
    return result

def get_shape(lay: pdk.TGIS_LayerVector, index: int) -> pdk.TGIS_Shape:
    i = 0
    for shp in lay.Loop():
        if i == index:
            return shp
        i += 1
    raise IndexError('get_shape: index out of range')

def tpath(path):
    """
    returns trailing path
    :param path:
    :return:
    """
    return path if path.endswith(os.sep) else path + os.sep

def is_file(path):
     return os.path.exists(path)



if __name__ == '__main__':
    jul = 2451545.0
    yyyy, MM, dd, hh, mm, ss = jd_to_calendar(jul)
    print(f'{yyyy}-{MM:02d}-{dd:02d} {hh:02d}:{mm:02d}:{ss:02d}')
    print(f' -- julian date to TDateTime via calendar {jul_to_date_field(jul)}')
    print(f' -- julian date to TDateTime direct {julian_to_tdatetime(jul)}')

    tdatetime = julian_to_tdatetime(jul)
    #tdatetime = 45250.0  # Delphi TDateTime for "2023-12-31"
    dt_np = tdatetime_to_datetime64_full(tdatetime)
    print(dt_np)  # Output: "2023-12-31"

# # Example usage:
# tdatetime_value = gregorian_to_tdatetime(2025, 2, 6, 2, 5, 22)
# print(f"TDateTime Value: {tdatetime_value}")


