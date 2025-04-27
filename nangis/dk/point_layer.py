# Created by mareko@hi.no at 03.03.2025

# Feature: # point layer creators
import tatukgis_pdk as pdk
import numpy as np
from typing import Union

def create_point_layer(name : str
                       , geometry : np.ndarray
                       , data: np.ndarray
                       , column_names : list
                       , cs : int = 4326  # Assuming EPSG:4326 for WGS84_LATLON
                       , skip_nan : bool = False
                       ) -> pdk.TGIS_LayerVector:
    """
     Create vector layer for point geometry and some fields
    : param name: layer name
    :param geometry:
    :param data:
    :param column_names:
    :param cs: EPSG code
    :param skip_nan:  whether to skip NaN values
    :return:
    """
    if geometry.ndim != 2:
        raise ValueError('ARG2: Geometry matrix must be a matrix')
    if geometry.shape[1] != 2:
        raise ValueError('ARG2: Geometry matrix must have 2 columns')
    if data.ndim != 2:
        raise ValueError('ARG2: Data  must be a matrix')
    if geometry.shape[0] != data.shape[0]:
        raise ValueError('ARG2, ARG2: Geometry and Data matrix must have same rows')
    if len(column_names) != data.shape[1]:
        raise ValueError('ARG3, ARG3: Number of columns must agree with the length of column names')



    lv = pdk.TGIS_LayerVector()
    lv.SetCSByEPSG(cs)
    lv.Name = name
    lv.Path = ''
    lv.Open()

    ncol = data.shape[1]


    nrow = data.shape[0]


    for i in range(ncol):
        lv.AddField(column_names[i], pdk.TGIS_FieldType().Float, 10, 4)

    for i in range(nrow):
        if not skip_nan:
            data[i, :] = np.nan_to_num(data[i, :])
        elif np.isnan(data[i, :]).any():
            continue  # Skip rows with NaNs

        shp = lv.CreateShape(pdk.TGIS_ShapeType().Point)
        shp.Lock(pdk.TGIS_Lock().Projection)
        shp.AddPart()
        shp.AddPoint(pdk.TGIS_Utils.GisPoint(geometry[i, 0], geometry[i, 1]))

        #for j in range(ncol):
        #    shp.SetField(column_names[j], dataaa[i, j])
        for name, value in zip(column_names, data[i]):
            shp.SetField(name, value)

        shp.Unlock()

    lv.RecalcExtent()
    return lv



