# Created by mareko@hi.no at 27.02.2025



# Description: #handles datsaet _ab
# This dataset  the following columns
#  LON - lon start
#  LAT - lat start
#  DATE  - date start
#  LON_B   lon stop
#  LAT_B   latitude stop
#  DATE_B  date stop

# writes the positional information as a 2 point arc

# Created by mareko@hi.no at 08.02.2025

# Dataset related operation

import numpy as np
#from tatukgis_pdk import TGIS_LayerVector, TGIS_ShapeType, TGIS_FieldType, TGIS_Utils, TGIS_Shape, TGIS_Lock
import tatukgis_pdk as pdk
from nangis.dk.os2dk import jdn2dk

def create_dataset_ab(
    name: str,
    data: np.ndarray,
    params: list,
    NaNsToZero: bool = False,
    fixedKeyField: str = '',
    fixedKeyValue: int = -1,
    CS: int = 4326  # Assuming EPSG:4326 for WGS84_LATLON
) -> pdk.TGIS_LayerVector:
    """
       Create a GIS vector layer for trawl-like dataaa which define line from start to stop
       The line is used as geometry only, LON, LAT fields contain the mean longitude latitude
       However, times are include both DATE_START and DATE_STOP

       :param name: Layer name.
       :type name: str
       :param data: A dataaa table where columns contain parameters and rows represent dataaa cycles.
       :type data: numpy.ndarray
       :param params: List of parameter names corresponding to the dataaa columns.
       :type params: list
       :param NaNsToZero: If True, forces NaN values to 0; otherwise, skips rows with NaNs. Defaults to False.
       :type NaNsToZero: bool, optional
       :param fixedKeyField: Name of a fixed value key field (e.g., 'SURVEY_NO'). If an empty string, this field is ignored. Defaults to ''.
       :type fixedKeyField: str, optional
       :param fixedKeyValue: Value assigned to the fixed key field. Defaults to -1.
       :type fixedKeyValue: int, optional
       :param ilonlatjday: A list of three indices specifying the positions of longitude, latitude, and Julian day in the dataaa columns. Defaults to [0, 1, 2] if not provided.
       :type ilonlatjday: list, optional
       :param CS: Coordinate system's EPSG code. Defaults to 4326 (WGS84).
       :type CS: int, optional
       :return: The created GIS vector layer.
       :rtype: TGIS_LayerVector
       :raises ValueError: If the number of columns in dataaa does not match the number of parameter names, or if ilonlatjday does not contain exactly three elements.
       """

    if data.shape[1] != len(params):
        raise ValueError('create_dataset_ab: Number of columns in dataaa does not match the number of parameter names')


    mILon, mILat, mIJday = 0, 1, 2
    mILon_b, mILat_b, mIJday_b = 3, 4, 5

    lv = pdk.TGIS_LayerVector()
    lv.SetCSByEPSG(CS)
    lv.Name = name
    lv.Path = ''
    lv.Open()

    Ncol = data.shape[1]
    if Ncol < 6:
        raise ValueError('create_layer: Number of columns must be at least 6')
    if Ncol != len(params):
        raise ValueError('create_layer: Number of columns does not match the number of parameter names')

    Nrow = data.shape[0]


    bFixedField = False
    if fixedKeyField:
        lv.AddField(fixedKeyField, pdk.TGIS_FieldType().Number, 10, 0)
        bFixedField = True

    lv.AddField('LON', pdk.TGIS_FieldType().Float, 10, 4) # central latitude as filed
    lv.AddField('LAT', pdk.TGIS_FieldType().Float, 10, 4)
    lv.AddField('DATE_START', pdk.TGIS_FieldType().Date, 10, 4)
   # lv.AddField('LON_B', pdk.TGIS_FieldType().Float, 10, 4)
   # lv.AddField('LAT_B', pdk.TGIS_FieldType().Float, 10, 4)
    lv.AddField('DATE_STOP', pdk.TGIS_FieldType().Date, 10, 4)
    for i in range(Ncol):
        if i in {mILon, mILat, mIJday, mILon_b, mILat_b, mILat_b, mIJday_b}:
            continue
        lv.AddField(params[i], pdk.TGIS_FieldType().Float, 10, 4)

    for i in range(Nrow):
        if NaNsToZero:
            data[i, :] = np.nan_to_num(data[i, :])
        elif np.isnan(data[i, :]).any():
            continue  # Skip rows with NaNs

        shp = lv.CreateShape(pdk.TGIS_ShapeType().Arc)
        shp.Lock(pdk.TGIS_Lock().Projection)
        shp.AddPart()
        shp.AddPoint(pdk.TGIS_Utils.GisPoint(data[i, mILon], data[i, mILat]))
        shp.AddPoint(pdk.TGIS_Utils.GisPoint(data[i, mILon_b], data[i, mILat_b]))

        if bFixedField:
            shp.SetField(fixedKeyField, fixedKeyValue)
            # we use center point as the parametr
        long =(data[i, mILon] + data[i, mILon_b]) * 0.5
        shp.SetField('LON', long)
        shp.SetField('LAT', (data[i, mILat] + data[i, mILat_b]) * 0.5)
        shp.SetField('DATE_START',jdn2dk(data[i, mIJday]))
        shp.SetField('DATE_STOP', jdn2dk(data[i, mIJday_b]))
        for j in range(Ncol):
            if j in {mILon, mILat, mIJday, mILon_b, mILat_b, mILat_b, mIJday_b}:
                continue
            shp.SetField(params[j], data[i, j])

        shp.Unlock()

    lv.RecalcExtent()
    return lv
