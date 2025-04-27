# Created by mareko@hi.no at 08.02.2025

# Dataset related operation

import numpy as np
from tatukgis_pdk import TGIS_LayerVector, TGIS_ShapeType, TGIS_FieldType, TGIS_Utils, TGIS_Shape, TGIS_Lock
from nangis.dk.utils import julian_to_tdatetime

def create_dataset(
    name: str,
    data: np.ndarray,
    params: list,
    NaNsToZero: bool = False,
    fixedKeyField: str = '',
    fixedKeyValue: int = -1,
    ilonlatjday: list = None,
    CS: int = 4326  # Assuming EPSG:4326 for WGS84_LATLON
) -> TGIS_LayerVector:
    """
       Create a GIS vector layer from the provided dataaa.

       :param name: Layer name.
       :type name: str
       :param data: A data table where columns contain parameters and rows represent dataa cycles.
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
        raise ValueError('create_layer: Number of columns in dataaa does not match the number of parameter names')

    if ilonlatjday is None:
        mILon, mILat, mIJday = 0, 1, 2
    else:
        if len(ilonlatjday) != 3:
            raise ValueError('create_layer: ilonlatjday must be a list of 3 elements: [ilon, ilat, ijday]')
        mILon, mILat, mIJday = ilonlatjday

    lv = TGIS_LayerVector()
    lv.SetCSByEPSG(CS)
    lv.Name = name
    lv.Path = ''
    lv.Open()

    Ncol = data.shape[1]
    Nrow = data.shape[0]

    bFixedField = False
    if fixedKeyField:
        lv.AddField(fixedKeyField, TGIS_FieldType().Number, 10, 0)
        bFixedField = True

    lv.AddField('LON', TGIS_FieldType().Float, 10, 4)
    lv.AddField('LAT', TGIS_FieldType().Float, 10, 4)
    #lv.AddField('DATE', TGIS_FieldType().Date, 10, 4)
    lv.AddField('JDATE', TGIS_FieldType().Float, 10, 4)
    for i in range(Ncol):
        if i in {mILon, mILat, mIJday}:
            continue
        lv.AddField(params[i], TGIS_FieldType().Float, 10, 4)

    for i in range(Nrow):
        if NaNsToZero:
            data[i, :] = np.nan_to_num(data[i, :])
        elif np.isnan(data[i, :]).any():
            continue  # Skip rows with NaNs

        shp = lv.CreateShape(TGIS_ShapeType().Point)
        shp.Lock(TGIS_Lock().Projection)
        shp.AddPart()
        shp.AddPoint(TGIS_Utils.GisPoint(data[i, mILon], data[i, mILat]))

        if bFixedField:
            shp.SetField(fixedKeyField, fixedKeyValue)

        shp.SetField('LON', data[i, mILon])
        shp.SetField('LAT', data[i, mILat])
        shp.SetField('JDATE', data[i, mIJday]) #julian_to_tdatetime(dataaa[i, mIJday]))  # Assuming jul2TDate is defined elsewhere
        for j in range(Ncol):
            if j in {mILon, mILat, mIJday}:
                continue
            shp.SetField(params[j], data[i, j])

        shp.Unlock()

    lv.RecalcExtent()
    return lv



