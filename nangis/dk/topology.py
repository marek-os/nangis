# toplogoy operations
import tatukgis_pdk as pdk
import math
#from tatukgis_pdk._lib.linux64.tatukgis_pdk import TGIS_ShapePolygon


def build_clipped_layer(source: pdk.TGIS_LayerVector, clip_extent: pdk.TGIS_Extent) -> pdk.TGIS_LayerVector:
    """
    This function is not used on the Delphi side. probably does not work
    @deprecated
    :param source:
    :param clip_extent:
    :return:
    """
    result = pdk.TGIS_LayerVector()
    result.name = source.name
    result.caption = source.caption
    result.SetCSbyEPSG(source.CS.EPSG)
    result.open()

    count = 0
    for shp in source.Loop(source.extent):
        clipped = shp.GetIntersection(clip_extent)
        if clipped is None:
            continue
        result.add_shape(clipped)
        count += 1

    if count == 0:
        return None
    else:
        result.recalc_extent()
        return result

def copy_clipped_layer(source: pdk.TGIS_LayerVector,
               clip_shape: pdk.TGIS_ShapePolygon,
               query: str = '') -> pdk.TGIS_LayerVector:
    """
    Returns an intersected (clipped) version of the source layer
    :param source:
    :param clip_shape:
    :param query:
    :return:
    """

    vec = pdk.TGIS_LayerVector()
    vec.name = source.name
    vec.SetCSByEPSG(source.CS.EPSG)
    vec.ImportStructure(source)

    vec.open()

    count = 0
    topo = pdk.TGIS_Topology()

    for shp in source.Loop(source.Extent, query):
        sout = topo.combine(
            shp,
            clip_shape,
            pdk.TGIS_TopologyCombineType().Intersection
        )
        if sout is not None:
            #sout.CopyFields(shp)
            ss = vec.AddShape(sout)
            ss.CopyFields(shp)
            count += 1

    if count == 0:
        return None
        # if not retain_missing:
        #     return None
        # else:
        #     pass # __add_dummy_shape(source, vec, clip_shape)

    vec.RecalcExtent()
    return vec

def exclude_layer_from_shape(shp : pdk.TGIS_ShapePolygon, layer : pdk.TGIS_LayerVector) -> pdk.TGIS_Shape:
    """
    formely mkDifferenceShape()
    Removes shape potions overallpeds with hapes of a layer
    :param shp: shape to modify
    :param layer: layer containing overapping shape portions
    :return: clipped layer
    """
    topo = pdk.TGIS_Topology()
    i = 0
    for tmp in layer.Loop():
        if i == 0:
            tmp2 = shp
        tmp3 = topo.Combine(tmp2, tmp, pdk.TGIS_TopologyCombineType().Difference)
        tmp2 = tmp3
        i += 1
    return tmp3

def build_shape_buffer(shp : pdk.TGIS_Shape, buff_length : float) -> pdk.TGIS_ShapePolygon:
    topo = pdk.TGIS_Topology()
    if math.fabs(buff_length) < 1e-10:
        return shp  # no buffer here
    return topo.MakeBuffer(shp, buff_length)

def build_layer_buffer(source : pdk.TGIS_LayerVector, buff_length : float) -> pdk.TGIS_LayerVector:
    """
    build buffer around shapes in polygon layer
    TODO: must include shape checks for pdk.TGIS_ShapeType().Polygon
    :param source:
    :param buff_length:
    :return:
    """
    vec = pdk.TGIS_LayerVector()
    vec.name = source.name
    vec.SetCSByEPSG(source.cs.epsg)
    vec.ImportStructure(source)
    vec.open()

    topo = pdk.TGIS_Topology()
    for shp in source.Loop(source.Extent):
        buf = topo.MakeBuffer(shp, buff_length)
        vec.AddShape(buf)
    return vec




