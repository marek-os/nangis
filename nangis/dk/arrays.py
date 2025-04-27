# Created by mareko@hi.no at 02.03.2025

# Feature: # dk to arrays conversions

import tatukgis_pdk as pdk
import numpy as np
from nangis.dk.utils import get_field_names, get_geometry
#__all__ = ["as_matrix"]

def as_matrix(layer: pdk.TGIS_LayerVector) -> np.ndarray:
    """
    converts field values from a layer to numpy matrix
    :param layer:
    :return:
    """
    col_names = get_field_names(layer)
    clen = len(col_names)
    buf = []
    for shp in layer.Loop():
        record = [shp.GetField(col_names[j]) for j in range(clen)]
        buf.append(record)
    return np.array(buf)

def as_vector(layer: pdk.TGIS_LayerVector, column : str) -> np.ndarray:
    col_names = get_field_names(layer)
    if not column in col_names:
        raise ValueError(f"column {column} not found in layer {layer.Name}")
    buf = []
    for shp in layer.Loop():
        val = shp.GetField(column)
        buf.append(val)
    return np.array(buf)

def as_geometry_matrix(layer: pdk.TGIS_LayerVector, part : int) -> np.ndarray:
    """
    converts layer's geometry to matrix (minimum 2 columns)
    :param layer: source layer with fixed gemoetry: points - equal size elements
    :param part: shape part
    :return: matrix rows n shapes columns - geometry
    """

    buf = []
    for shp in layer.Loop():
        geom = get_geometry(shp, part)
        buf.append(geom)

    return np.array(buf)





