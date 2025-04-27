#function helping to create simulation
import tatukgis_pdk as pdk
from nangis.dk.utils_lvector import new_layer_rectangle
from nangis.dk.factories.voronoi_factory import build_voronoi_map
from nangis.dk.utils import get_shape
from nangis.dk.topology import build_shape_buffer, copy_clipped_layer
from nangis.dk.integrator import integrate_lat_strip, get_integrator_field_names
import numpy as np


def build_voronoi_over_stratum(ldata: pdk.TGIS_LayerVector,  lstratum : pdk.TGIS_LayerVector) -> pdk.TGIS_LayerVector:
    """
    Builds Voronoi diagram over stratum
    :param ldata:
    :param lstratum:
    :return:
    """
    shp = get_shape(lstratum, 0)
    return build_voronoi_map(ldata,shp)


def build_clip_over_stratum_and_coast(lstratum : pdk.TGIS_LayerVector
                                     , lcoast : pdk.TGIS_LayerVector) -> pdk.TGIS_LayerVector:
    """
    Creates rectangulear stratum for voronoi rectangle.
    It extends from the east of he stratum to the costline in the east
    :param lstratum:
    :param lcoast:
    :return:
    """
    ext = pdk.TGIS_Extent()
    ext.XMin = lstratum.Extent.XMin - 1.0/60
    ext.XMax = 14.0 #  roughly the coast boundarylcoast.Extent.XMin + 1.0/60
    ext.YMin = lstratum.Extent.YMin
    ext.YMax = lstratum.Extent.YMax
    return new_layer_rectangle('STRATUM_TO_CLIP_VORONOI', ext)

def build_rectangular_voronoi(ldata : pdk.TGIS_LayerVector,
                         lstratum : pdk.TGIS_LayerVector,
                         lcoast : pdk.TGIS_LayerVector) -> pdk.TGIS_LayerVector:
    """

    :param ldata:
    :param lstratum:
    :param lcoast:
    :return:
    """
    clipper = build_clip_over_stratum_and_coast(lstratum, lcoast)
    shp = get_shape(clipper, 0)
    return build_voronoi_map(ldata, shp)

def integrate_nansen_region(rect_vor : pdk.TGIS_LayerVector
                             , stratum : pdk.TGIS_Shape
                             , bufMin : float = -1.0
                             , bufMax : float = 1.0
                             , bufStep : float = 0.01
                             )  :

    li_nort = []
    li_cent = []
    li_sout = []
      # kilometers to degrees
    bufMin = bufMin * 0.008999928
    bufMax = bufMax * 0.008999928
    bufStep = bufStep * 0.008999928

    for gl in np.arange(bufMin, bufMax + bufStep, bufStep):
        #print(f'processing {gl}: {gl/(bufMax - bufMin)*100}%')
        buf = build_shape_buffer(stratum, gl)
        lvor = copy_clipped_layer(rect_vor, buf)
        north = integrate_lat_strip(lvor, ['FISH_SA'], -9.0, -6.0)
        central = integrate_lat_strip(lvor, ['FISH_SA'], -12.5, -9.0)
        south = integrate_lat_strip(lvor, ['FISH_SA'], 17.25, -12.5)
        li_nort.append(north)
        li_cent.append(central)
        li_sout.append(south)
    it_names = get_integrator_field_names(['FISH_SA'])
    print(f'Integrator field names: {it_names}')
    return np.array(li_nort), np.array(li_cent), np.array(li_sout)





