# Created by mareko@hi.no at 08.02.2025

# Stratum related operations

import tatukgis_pdk as pdk
from nangis.dk.utils import get_shape_by_column_value, get_shape
#from tatukgis_pdk._lib.linux64.tatukgis_pdk import TGIS_LayerVector


def get_stratum_item_by_name(stratum_layer : pdk.TGIS_LayerVector, name ) -> pdk.TGIS_Shape:
    """
     return stratum with the stratum_name created with function below
    :param stratum_layer: stratum layer 
    :param name: item of this stratum with name set in create_stratum_over_data
    :return: stratum polygon or None
    """
    return get_shape_by_column_value(stratum_layer, 'STRATUM', name)

def create_stratum_over_data(dframe : pdk.TGIS_LayerVector
                             ,stratum_name : str
                             , coast: pdk.TGIS_LayerVector = None
                             ,tolerance: float = 0.7
                             , buffer_width: float = 0
                             ) -> pdk.TGIS_LayerVector:
    """
     Creates new stratum layer as convex hull over dataaa
    :param dframe:  dataaa frame layer for which stratum will be created
    :param stratum_name: name of new stratum
    :param tolerance: toklerace parameter
    :param buffer_width: buffer width
    :param coast: coast layer used to limit the convex hull around the dataaa
    :return:
    """
    if dframe.CS.EPSG == 4326:  # WGS84
        buffer_width = buffer_width * 0.008999928 # km to degrees here it must be in degrees

    stratum = pdk.TGIS_LayerVector()
    stratum.SetCSByEPSG(dframe.CS.EPSG)
    stratum.name = stratum_name;
    stratum.Caption = stratum_name;
    stratum.AddField('STRATUM', pdk.TGIS_FieldType().String, 1, 0);

    topo = pdk.TGIS_Topology()
    poly = topo.ConcaveHull(dframe, tolerance)
    if buffer_width != 0:
        poly = topo.MakeBuffer(poly, buffer_width)
    if coast is not None:
        cpoly = cut_polygon_parts_inside_other_stratum(topo, poly, coast)
        lpoly = stratum.addShape(cpoly)
        lpoly.SetField('STRATUM', stratum_name);
    return stratum

def exclude_coast_from_stratum(stratum : pdk.TGIS_LayerVector
                             , coast: pdk.TGIS_LayerVector
                             , new_stratum_name: str = ''
                             , buffer_width: float = 0
                             ) -> pdk.TGIS_LayerVector:
    """
     excludes coast layer from astratum - works on the sigle stratum layers only
    :param dframe:  dataaa frame layer for which stratum will be created
    :param stratum_name: name of new stratum
    :param tolerance: toklerace parameter
    :param buffer_width: buffer width
    :param coast: coast layer used to limit the convex hull around the dataaa
    :return:
    """
    if stratum.CS.EPSG == 4326:  # WGS84
        buffer_width = buffer_width * 0.008999928 # km to degrees here it must be in degrees

    stratum2 = pdk.TGIS_LayerVector()
    stratum2.SetCSByEPSG(stratum.CS.EPSG)
    stratum2.AddField('STRATUM', pdk.TGIS_FieldType().String, 1, 0)

    if new_stratum_name != '':
        stratum2.Name = new_stratum_name
    else:
        stratum2.Name = stratum.Name + '_NO_COAST'

    topo = pdk.TGIS_Topology()
    poly = get_shape(stratum, 0) # first stratum only
    if buffer_width != 0:
        poly = topo.MakeBuffer(poly, buffer_width)
    if coast is not None:
        cpoly = cut_polygon_parts_inside_other_stratum(topo, poly, coast)
        lpoly = stratum2.addShape(cpoly)
        lpoly.SetField('STRATUM', stratum.Name)
    return stratum2


def cut_polygon_parts_inside_other_stratum(topo : pdk.TGIS_Topology,
                                           polygon_to_cut : pdk.TGIS_Shape,
                                           other_stratum : pdk.TGIS_LayerVector,
                                           ) -> pdk.TGIS_Shape:
    """
    Creates difference shape C = shapeA - stratumB
     stratum instead of shape because we iterate over all polygon shape withing that stratum
    :param topo: topology object
    :param polygon_to_cut: shape A
    :param other_stratum: stratum B (all shapes within this stratum)
    :return: the trimmed polygon C
    """
    #topo = pdk.TGIS_Topology()
    i = 0
    for tmp1 in other_stratum.Loop():
        if i == 0:
            tmp2 = polygon_to_cut # we chip off the original polygon bit by bit
        tmp3 = topo.Combine(tmp2, tmp1, pdk.TGIS_TopologyCombineType().Difference)
        if tmp3 is not None:
            tmp2 = tmp3
        i = i + 1
    return tmp3





