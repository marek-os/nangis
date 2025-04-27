# styles for comscatter layer
import tatukgis_pdk as pdk
import numpy as np
from nangis.dk.styles.color_names import TCm, dk_color
def set_style_nansen_report(lay: pdk.TGIS_LayerVector
                            ,field_name: str
                            , size: int = 200
                            , opacity: float = 50
                            , which_labels: int = 0
                            ) ->None:
    if field_name.startswith('SP1') or field_name.startswith('SP2'):
        mlrg = np.array(['0', '100', '1000', '3000', '10000', '30000', '100000', '300000000'])
    else:
        mlrg = np.array(['0', '1', '100', '300', '1000', '3000', '10000', '30000000'])

    li = lay.ParamsList
    li.Clear()

    pr = __last(li)
    pr.Legend = mlrg[0]
    pr.Query = field_name + ' < ' + mlrg[1]


    pr.Marker.Style = pdk.TGIS_MarkerStyle().Cross
    pr.Marker.Size = size // 2
    pr.Marker.Color = pdk.TGIS_Color.LightGray
    pr.Marker.OutlineWidth =  size // 20
    pr.Marker.OutlineColor = pdk.TGIS_Color.Gray
    pr.Marker.ShowLegend = True

    pr.labels.Visible = False

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[1] + ' - ' + mlrg[2]
    pr.Query  = field_name + ' >= ' + mlrg[1] + ' AND ' + field_name + ' < ' + mlrg[2]
    __set_params(pr, field_name, TCm.Navy, size, opacity, which_labels)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[2] + ' - ' + mlrg[3]
    pr.Query  = field_name + ' >= ' + mlrg[2] + ' AND ' + field_name + ' < ' + mlrg[3]
    __set_params(pr, field_name, TCm.Blue, size, opacity, which_labels)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[3] + ' - ' + mlrg[3]
    pr.Query  = field_name + ' >= ' + mlrg[3] + ' AND ' + field_name + ' < ' + mlrg[4]
    __set_params(pr, field_name, TCm.Green, size, opacity, which_labels)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[4] + ' - ' + mlrg[5]
    pr.Query  = field_name + ' >= ' + mlrg[4] + ' AND ' + field_name + ' < ' + mlrg[5]
    __set_params(pr, field_name, TCm.Yellow, size, opacity, which_labels)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[5] + ' - ' + mlrg[6]
    pr.Query  = field_name + ' >= ' + mlrg[5] + ' AND ' + field_name + ' < ' + mlrg[6]

    __set_params(pr, field_name, TCm.Red, size, opacity, which_labels)

    li.Add()
    pr = __last(li)
    pr.Legend = ' >= ' + mlrg[6]
    pr.Query  = field_name + ' >= ' + mlrg[6] + ' AND ' + field_name + ' < ' + mlrg[7]

    __set_params(pr, field_name, TCm.Purple, size, opacity, which_labels);


def __set_params(pr, field_name, color, size, opacity, which_labels):
    pr.Marker.Style = pdk.TGIS_MarkerStyle().Circle
    pr.Marker.Size =  size
    pr.Marker.Color = dk_color(color, opacity)
    pr.Marker.OutlineWidth = size // 15
    pr.Marker.OutlineColor = pdk.TGIS_Color.Black
    pr.Marker.ShowLegend = True

    if which_labels == 0:
        fieldID = field_name
    elif which_labels == 1:
        fieldID = 'DEPTH'
    else:
        fieldID = field_name
        pr.labels.visible = False

    pr.labels.Visible = True;
    pr.Labels.Field = fieldID
    pr.Labels.Value =  '{' + fieldID + ':D1}' # "{%s:01d}" % fieldID
    pr.Labels.Pattern = pdk.TGIS_BrushStyle.Clear
    pr.Labels.OutlineWidth = 0
    pr.Labels.Font.Color = pdk.TGIS_Color.White
    pr.Labels.Color = pdk.TGIS_Color.Black


def __last(li):
    return li.Items(li.Count - 1)




