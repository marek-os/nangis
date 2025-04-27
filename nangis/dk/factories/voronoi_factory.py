# creates voronoi diagrams
import tatukgis_pdk as pdk
from nangis.dk.topology import copy_clipped_layer
def build_voronoi_map( ldata : pdk.TGIS_LayerVector
                        ,clipPolygon: pdk.TGIS_Shape
                        , query : str = ''
                       ) -> pdk.TGIS_LayerVector:
    lVrn = pdk.TGIS_LayerVoronoi()
    lVrn.SetCSByEPSG(ldata.CS.EPSG)
    lVrn.ImportLayer(ldata, clipPolygon.Extent,   # use the extent of the polygon
                    pdk.TGIS_ShapeType().Unknown
                    , query
                     , True    # true to make voronoi to full extent
                   )
    res = copy_clipped_layer(lVrn, clipPolygon)
    if res is None:
        raise ValueError('Could not create voronoi map for the input dataaa: clipPolygon outside?')
    return res





