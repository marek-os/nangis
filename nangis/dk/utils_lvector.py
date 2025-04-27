# layer and shape utils
import tatukgis_pdk as pdk
from typing import List
import os
def new_shape_rectangle(oParent: pdk.TGIS_LayerVector, oExtent: pdk.TGIS_Extent) -> pdk.TGIS_Shape:
    oShape = oParent.CreateShape(pdk.TGIS_ShapeType().Polygon)

    oShape.Lock(pdk.TGIS_Lock().Projection)
    oShape.AddPart()

    oShape.AddPoint(pdk.TGIS_Utils.GisPoint(oExtent.XMin, oExtent.YMin))
    oShape.AddPoint(pdk.TGIS_Utils.GisPoint(oExtent.XMax, oExtent.YMin))
    oShape.AddPoint(pdk.TGIS_Utils.GisPoint(oExtent.XMax, oExtent.YMax))
    oShape.AddPoint(pdk.TGIS_Utils.GisPoint(oExtent.XMin, oExtent.YMax))
    oShape.AddPoint(pdk.TGIS_Utils.GisPoint(oExtent.XMin, oExtent.YMin))  # close polygon

    oShape.Unlock()

    return oShape

def new_layer_rectangle(sLayerName: str, oExtent: pdk.TGIS_Extent, nEPSG: int = 4326) -> pdk.TGIS_LayerVector:
    oLayer = pdk.TGIS_LayerVector()
    oLayer.Open()

    oLayer.SetCSByEPSG(nEPSG)
    oLayer.Name = sLayerName
    oLayer.Caption = sLayerName

    oLayer.AddField("TYPE", pdk.TGIS_FieldType().String, 1, 0)

    oShape = new_shape_rectangle(oLayer, oExtent)
    oShape.SetField("TYPE", "RECTANGLE")

    oLayer.Params.Area.Color = pdk.TGIS_Color.Yellow
    oLayer.Params.Area.OutlineWidth = 0
    oLayer.DefaultShapeType = pdk.TGIS_ShapeType.Polygon
    oLayer.Transparency = 50
    oLayer.Params.Area.OutlineWidth = 20
    oLayer.Params.Area.OutlineColor = pdk.TGIS_Color.Blue

    return oLayer

def get_uids(oLayer: pdk.TGIS_LayerVector) -> List[int]:
    return [oShape.Uid for oShape in oLayer.Loop()]

def save_shp(layer: pdk.TGIS_LayerVector, file_name: str, overwrite: bool = False) -> None:
    shp_path = file_name if file_name.lower().endswith(".shp") else file_name + ".shp"

    if os.path.isfile(shp_path) and (not overwrite):
        raise IOError(f"save_shp: Target SHP file exists — must delete it first: {shp_path}")

    outlay = pdk.TGIS_LayerSHP()
    outlay.Path = file_name

    layer.ExportLayer(
        outlay,
        layer.Extent,
        pdk.TGIS_ShapeType().Unknown,
        "",
        False
    )

def load_shp(file_name: str, layer_name: str = "") -> pdk.TGIS_Layer:
    """
    Load a SHP file into a TatukGIS layer.

    Parameters:
        file_name (str): Path to the .shp file.
        layer_name (str): Optional layer name. If not provided, basename is used.

    Returns:
        TGIS_Layer: The loaded SHP layer.

    Raises:
        RuntimeError: If the file does not exist or loading fails.
    """
    if not os.path.isfile(file_name):
        raise IOError("[loadSHP] ARG1: input file not found")

    nam = os.path.splitext(os.path.basename(file_name))[0] if layer_name == "" else layer_name

    lay = pdk.TGIS_LayerSHP() #pdk.TGIS_Utils.GisCreateLayer(nam, file_name))
    lay.Path = file_name
    lay.Open()

    if lay is None:
        raise IOError("[loadSHP] ARG1: failed to load SHP file. Is format correct?")

    return lay
