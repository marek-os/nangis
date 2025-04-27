# integrates layer inside shape
import tatukgis_pdk as pdk
from typing import Dict, Union, List
from nangis.dk.utils_lvector import new_layer_rectangle, get_uids
from nangis.dk.utils import get_field_names, get_shape
from nangis.dk.topology import  copy_clipped_layer
from nangis.dk.stats import integrate
LON = 0
LAT = 1
_JDAY = 2
LOG_MIN=3
LOG_MAX=4
DEPTH=5
FISHCAT_OFFSET = 6

cPOLYIG_AREA_COVERED='AREA_COVERED'
cPOLYIG_N_POLYGONS= 'N_POLYGONS'
cPOLYIG_FRINGE_NO= 'FRINGE_NO'
cPOLYIG_LAT0='LAT0'
cPOLYIG_SURVEY_NO = 'SURVEY_NO'
cPOLYIG_DATE = 'DATE'


#def integrate_voronoi(vor : pdk.TGIS_LayerVector, clip_shape : pdk.TGIS_Shape) -> Dict[str, Union[str, int, float]]:
def integrate_layer(vor : pdk.TGIS_LayerVector
                    , fields: List[str]
                    , clip_shape : pdk.TGIS_Shape
                    , units: str = 'nm'
                    ) -> List[float]:
    """
    integrates all polygonal shapes within avor are aclipped by clip_shape
    :param vor: source vector layer, typically voronoi map
    :param fields: field names for the vector layer to integrate
    :param clip_shape: clip shape to the region within  from the source to preform integration
    :param units: are units: squared nm - nautical default or suqted kilometer
    :return: the list containing integrals and areas for considered fields
    """
    clipped_area = copy_clipped_layer(vor, clip_shape)
    return integrate(clipped_area, fields, units, 0)


def integrate_lat_strip(vor : pdk.TGIS_LayerVector, fields: List[str], lmin: float, lmax: float) -> List[float]:
    """
    Integrates over a latitudinal strip. The longitudinal extent matches the extent of the Voronoi layer.

    :param vor: Voronoi polygon layer (e.g., pdk.TGIS_LayerVector)
    :param fields: List of field names to integrate
    :param lmin: Minimum latitude
    :param lmax: Maximum latitude
    :return: A list containing:
        - Total area integrated (in nautical miles²)
        - Number of polygons included
        - Integral of each field (area-weighted sum)
        -  Non-zero area for each field
    """
    ext = pdk.TGIS_Extent()
    ext.XMin = vor.Extent.XMin
    ext.XMax = vor.Extent.XMax
    ext.YMin = float(lmin)
    ext.YMax = float(lmax)
    lay = new_layer_rectangle('LAT_FRINGE', ext)
    return integrate_layer(vor, fields, get_shape(lay, 0))

def get_integrator_field_names(field_names: List[str]) -> List[str]:
    """
    Returns output integrator field names
    :param field_names: names of fields to integrate
    :return: names of fields integrator creates
    """
    ls = ['AREA_COVERED', 'N_POLYGONS']
    for fl in field_names:
        ls.append(fl)
        ls.append(fl + '_AREA')
    return ls



