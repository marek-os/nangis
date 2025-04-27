# pandas TGIDS_Layer field convertion

from nangis.dk.utils import get_field_names, tdatetime_to_np
import tatukgis_pdk as pdk
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
import numpy as np

def as_dataframe(layer: pdk.TGIS_LayerVector) -> pd.DataFrame:
    """
    Converts fields vector layer to dataaa frame
    applicable to dataaa frame layer types (
    :param layer: pdk layer vector
    :return:  pandas dataaa farme
    """
    col_names = get_field_names(layer)
    # look for date field
    buf = np.full(layer.Fields.Count, False, dtype=bool)
    i = 0
    jdate_index = -1
    for fld in layer.Fields:
        if fld.Name == 'JDATE':
            buf[i] = True
            jdate_index = i
            break
        i = i + 1
    cnt = len(col_names)
    records = []
    i = 0
    for shp in layer.Loop():
        #record = [shp.GetField(col_names[j]) for j in range(cnt)]
        record = []
        for j in range(cnt):
            val = shp.GetField(col_names[j])
            if buf[j] == True:
                #print(f'{i}   -- {val}')
                val = pd.to_datetime((val - 2440587.5) * 86400, unit='s')

            record.append(val)
        records.append(record)
    if jdate_index >= 0:
        col_names[jdate_index] = 'DATE_TIME'
    return pd.DataFrame(records, columns=col_names)


def as_vectorlayer(df: pd.DataFrame
                   , layer_name: str = 'LAYER_PANDAS'
                   , lonName: str = 'LON'
                   , latName: str = 'LAT'
                   , dtName: str = 'DATE_TIME'
                   , CS: int = 4326  # Assuming EPSG:4326 for WGS84_LATLON
                   ) -> pdk.TGIS_LayerVector:
    """

    :param df:
    :return:
    """
    required_columns = {lonName, latName}
    if not required_columns.issubset(df.columns):
        raise ValueError('ARG1: Required columns LON and LAT not present in DataFrame')
    jdate_index = first_timestamp_index(df)
    lon_index = column_index_of(df, lonName)
    lat_index = column_index_of(df, latName)

     # Define Pandas to TGIS field type mapping
    dtype_map = {
        'int64': pdk.TGIS_FieldType().Number,
        'float64': pdk.TGIS_FieldType().Float,
        'object': pdk.TGIS_FieldType().String,
        'bool': pdk.TGIS_FieldType().Boolean,
        'datetime64[ns]': pdk.TGIS_FieldType().Date  # Default, but we'll override 'DATE_TIME'
    }



    lv = pdk.TGIS_LayerVector()
    lv.SetCSByEPSG(CS)
    lv.Name = layer_name
    lv.Path = ''
    lv.Open()

    for col in df.columns:
        # Handle special case for 'DATE_TIME' → 'JDATE' as Float
        if col == dtName and df[col].dtype == 'datetime64[ns]':
            lv.AddField('JDATE', pdk.TGIS_FieldType().Float, 10, 4)  # Store as float
        else:
            pandas_dtype = str(df[col].dtype)
            gis_type = dtype_map[pandas_dtype] if pandas_dtype in dtype_map else pdk.TGIS_FieldType().String
            #gis_type = dtype_map.get(pandas_dtype, pdk.TGIS_FieldType().String)  # Default to string

            lv.addField(col, gis_type, 10, 4)




    for _, row in df.iterrows():
        shp = lv.CreateShape(pdk.TGIS_ShapeType().Point)
        shp.Lock(pdk.TGIS_Lock().Projection)
        shp.AddPart()
        shp.AddPoint(pdk.TGIS_Utils.GisPoint(
              row[lonName]
            , row[latName]
        ))
         # Convert 'DATE_TIME' to Julian Date if present
        for col in df.columns:
            if col == dtName and df[col].dtype == 'datetime64[ns]':
                jdate = row[col].timestamp() / 86400 + 2440587.5  # Convert to Julian Date
                shp.SetField('JDATE', jdate)
            else:
                # Assign values based on type without unnecessary string conversion
                value = row[col]

                if pd.isna(value):  # Handle missing values
                    value = None
                elif isinstance(value, pd.Timestamp):
                    if dtype_map.get(str(df[col].dtype)) == pdk.TGIS_FieldType().Date:
                        value = value.to_pydatetime()  # Convert to Python datetime (TGIS_FieldType.Date)
                    else:
                        value = value.timestamp() / 86400 + 2440587.5  # Convert to Julian Date if required
                elif isinstance(value, (int, float, bool)):
                    pass  # Keep numeric and boolean values as-is
                else:
                    value = str(value)  # Convert everything else to string

                shp.SetField(col, value)
        shp.Unlock()

    lv.RecalcExtent()
    return lv


def as_stratum(df: pd.DataFrame
                   , layer_name:str = 'STRATA_PANDAS'
                   , stratum_name:str = 'STRATUM1'
                   , CS: int = 4326  # Assuming EPSG:4326 for WGS84_LATLON
                   , lonName : str = 'LON'
                   , latName : str = 'LAT',
                   ) -> pdk.TGIS_LayerVector:
    """

    :param df:
    :return:
    """
    required_columns = {lonName, latName}
    if not required_columns.issubset(df.columns):
        raise ValueError('ARG1: Required columns LON and LAT not present in DataFrame')


    lv = pdk.TGIS_LayerVector()
    lv.SetCSByEPSG(CS)
    lv.Name = layer_name
    lv.Path = ''
    lv.Open()


    lv.addField('STRATUM',  pdk.TGIS_FieldType().String, 10, 4)



    shp = lv.CreateShape(pdk.TGIS_ShapeType().Polygon)
    shp.Lock(pdk.TGIS_Lock().Projection)
    shp.AddPart()
    for _, row in df.iterrows():

        shp.AddPoint(pdk.TGIS_Utils.GisPoint(
              row[lonName]
            , row[latName]
        ))

        shp.Unlock()
    shp.SetField('STRATUM', stratum_name)

    return lv


def first_timestamp_index(df):
    """
    Returns the index of the first column with Timestamp type in a DataFrame.
    If no Timestamp column is found, returns -1.
    """
    return next((i for i, col in enumerate(df.columns) if is_datetime64_any_dtype(df[col])), -1)

def column_index_of(df, column_name):
    """
    Returns the index of the first column with the given name in a DataFrame.
    If the column is not found, returns -1.

    Parameters:
    df (pd.DataFrame): The DataFrame to search in.
    column_name (str): The name of the column to find.

    Returns:
    int: The index of the first matching column, or -1 if not found.
    """
    try:
        return df.columns.get_loc(column_name)
    except KeyError:
        return -1  # Column not found
