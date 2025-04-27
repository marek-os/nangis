# 2025-02-04 mapset class
#  hadling local files stored as sqlite

import os
import tatukgis_pdk as pdk
from typing import Union
import nangis.dk.db.dkio as SqliteLayer
import nangis.dk.basemap.map_layer_names as BLayer
import nangis.dk.utils as dutils

def begin_load(gis: Union[pdk.TGIS_Viewer, pdk.TGIS_ViewerWnd], path: str) -> bool:
    if not os.path.isfile(path):
        raise RuntimeError('begin_load: ARG1: file not found')

    # Open the vector layer
    vl = SqliteLayer.open_layer_vector(path, BLayer.LAYER_COASTLINE)


    # Close the current GIS project/view
    gis.Close()

    if vl  is not None:
        # Add the vector layer to the GIS viewer (PascalCase method)
        gis.Add(vl)
        vl.Caption = BLayer.CAP_LAND_MASSES

    borders = SqliteLayer.open_layer_vector(path, BLayer.LAYER_COUNTRY_BORDERS)
    if borders is not None:
        gis.Add(borders)
        borders.Caption = BLayer.CAP_COUNTRY_BORDERS


    # Set the coordinate system (WGS84 LAT/LON)
    vl.SetCSByEPSG(4326)

    return True

def get_layer_coastline(gis : pdk.TGIS_ViewerWnd) -> pdk.TGIS_LayerVector:
    return gis.Get(BLayer.LAYER_COASTLINE)


def end_load(gis: Union[pdk.TGIS_Viewer, pdk.TGIS_ViewerWnd], path: str) -> bool:

    # Replace qc with sqlite if needed (assuming it's already done externally)


    # Check if the file exists
    if not os.path.isfile(path):
        return False

    # Open the pixel layer from the SQLite file

    result = SqliteLayer.open_pixel_layer(path, "DEM")
   
    #print(f'----- Loaded  bathymetry {result} -----')

    # If the layer couldn't be opened, exit early
    if not result:
        return False



    # Set the layer in the GIS viewer
    dutils.set_layer(gis, result)

    # Set properties
    result.ZOrder = 999999
    result.Caption = "Bathymetry: GEBCO 2024"
    result.SetCSByEPSG(4326)
    return True

def load(gis: Union[pdk.TGIS_Viewer, pdk.TGIS_ViewerWnd], path: str) -> bool:
    gis.Lock()
    if not begin_load(gis, path):
        #print('!!! failed to load  coastline')
        return False
    #print('+++ Coastline loaded')
    ok = end_load(gis, path)
    gis.Unlock()
    if not ok:
         #print('!!! failed to load  bathymetry')
         return False
    else:
        #print('+++ bathymetry loaded')
        return True






