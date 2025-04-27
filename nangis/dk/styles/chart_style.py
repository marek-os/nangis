# Created by mareko@hi.no at 03.03.2025

# Feature: # assign chart styles
# Enter feature description here

import tatukgis_pdk as pdk  # Ensure TatukGIS PDK is imported
from nangis.dk.styles.color_names import TCm, dk_color
def set_pie_chart_style(ll : pdk.TGIS_LayerVector
                        , label_column : str
                        , sizing_column: str
                        , charted_columns : list
                        , data_range : list
                        , scale_range: list = [600, 600]
                        ) -> None:
    ll.UseConfig = False
    li = ll.ParamsList
    li.Clear()
    pr = li.Items(0)
    pr.Query = sizing_column + ' > 0'
    pr.Labels.Field = label_column
    pr.Labels.Pattern = pdk.TGIS_BrushStyle().Clear
    pr.Labels.OutlineWidth = 0
    pr.Labels.FontColor = pdk.TGIS_Color().White
    pr.Labels.FontSize = 200
    pr.Labels.Color = pdk.TGIS_Color().Black
    pr.Labels.Position = [pdk.TGIS_LabelPosition().MiddleCenter or pdk.TGIS_LabelPosition().Flow]
    pr.Chart.Size = pdk.TGIS_Utils.GIS_RENDER_SIZE()
    pr.Render.StartSize = scale_range[0]  # 350   this decides on pie chart size
    pr.Render.EndSize = scale_range[1]  # 1000
    # render results
    pr.Render.Expression = sizing_column
    pr.Render.Chart = "0:0:" + ":".join(charted_columns)
    pr.Chart.Style = pdk.TGIS_Utils.ParamChart('Pie', pdk.TGIS_ChartStyle().Pie)
    pr.Render.Zones = len(charted_columns)
    pr.Render.MinVal = data_range[0]
    pr.Render.MaxVal = data_range[1]

    #ll.Params.Chart.ShowLegend = True
    pr.Chart.Values = "0:0" + ":".join(charted_columns)
    pr.Chart.Legend = size_classes_to_labels( pr.Chart.Values)
    li.Add()
    pr = li.Items(1)
    pr.Query = sizing_column + ' <= 0'
    pr.Marker.Style = pdk.TGIS_MarkerStyle().Box  #DiagCross
    pr.Marker.Size = 200
    pr.Marker.Color = pdk.TGIS_Color.LightGray # dk_color(TCm.LightGray, 100)
    pr.Marker.OutlineWidth = pr.Marker.Size // 5
    pr.Marker.OutlineColor = pdk.TGIS_Color.Gray
    pr.Marker.ShowLegend = True



def size_classes_to_labels(input_str: str) -> str:
    parts = input_str.split(':')
    out_parts = []

    for i, token in enumerate(parts):
        if i < 2 or not token.startswith('R'):
            # Keep the first two elements as-is
            out_parts.append(token)
            continue

        token = token[1:]  # remove 'R'

        if '_INF' in token:
            start_val = int(token.split('_')[0])
            translated = f'> {start_val - 1}cm'
        else:
            start_val, end_val = map(int, token.split('_'))
            if i == 2:
                translated = f'< {end_val + 1}cm'
            else:
                translated = f'{start_val}-{end_val}cm'

        out_parts.append(translated)

    return ':'.join(out_parts)


# def _set_pie_chart(params: pdk.TGIS_ParamsSectionVector, size_field: str, mi: float, ma: float,
#                   member_fields: str, start_size: int, stop_size: int, levels: int, want_scale: bool):
#     """
#     Configures a Pie Chart in TatukGIS layer rendering parameters.
#
#     Parameters:
#     - params (pdk.TGIS_ParamsSectionVector): GIS vector layer parameters.
#     - size_field (str): Expression defining the size of the pie chart.
#     - mi (float): Minimum value for rendering.
#     - ma (float): Maximum value for rendering.
#     - member_fields (str): Member field values (e.g., '0:0:SARD:HORSE').
#     - start_size (int): Initial size of the pie chart markers.
#     - stop_size (int): Final size of the pie chart markers.
#     - levels (int): Number of scaling zones.
#     - want_scale (bool): Whether to show the scale/legend.
#     """
#
#     params.Chart.Size = pdk.GIS_RENDER_SIZE  # Equivalent constant in PDK
#
#     params.Render.StartSize = start_size
#     params.Render.EndSize = stop_size
#
#     params.Render.Expression = size_field
#     params.Render.Chart = member_fields  # e.g., '0:0:SARD:HORSE'
#
#     params.Chart.Style =  pdk.TGIS_Utils.ParamChart("Pie", pdk.TGIS_ChartStyle.Pie)
#
#     params.Render.Zones = levels
#     params.Render.MinVal = mi
#     params.Render.MaxVal = ma
#     params.Area.ShowLegend = want_scale
#     params.Marker.Size = 0  # Ensure markers do not overlap


