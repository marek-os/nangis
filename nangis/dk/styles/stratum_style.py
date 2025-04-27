# style for displaying stratum
import tatukgis_pdk as pdk
def set_stratum_yellow_semitransparent(lay : pdk.TGIS_LayerVector) -> None:
    lay.Params.Area.Color = pdk.TGIS_Color.Yellow;
    lay.Params.Area.OutlineWidth = 0
    lay.DefaultShapeType = pdk.TGIS_ShapeType.Polygon
    lay.Transparency = 18
    #lay.Params.Area.Pattern := TGIS_Brush.
    lay.Params.Area.OutlineWidth = 40;
    lay.Params.Area.OutlineColor = pdk.TGIS_Color.Red;  # TGIS_Color.Blue;
    lay.Params.Line.ShowLegend = False
    lay.Params.Marker.ShowLegend = False
    lay.Params.Area.ShowLegend = False
