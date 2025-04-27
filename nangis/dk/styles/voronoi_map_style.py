# style of voronoi maps
import tatukgis_pdk as pdk
import numpy as np
from nangis.dk.styles.color_names import TCm, dk_color
def set_style_nansen_voronoi_map(lay: pdk.TGIS_LayerVector
                                 , field_name: str
                                 , line_width: int = 15
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
    __set_params(pr, TCm.Blue, line_width, 1)
    #pr.Area.Pattern = pdk.TGIS_BrushStyle().Clear
   # alpha = int(255 * 5 / 100)  # 15% → 38
   # pr.Area.Color = pdk.TGIS_Color.FromARGB(alpha, 128, 128, 128)



    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[1] + ' - ' + mlrg[2]
    pr.Query  = field_name + ' >= ' + mlrg[1] + ' AND ' + field_name + ' < ' + mlrg[2]
    __set_params(pr, TCm.Navy, line_width, opacity)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[2] + ' - ' + mlrg[3]
    pr.Query  = field_name + ' >= ' + mlrg[2] + ' AND ' + field_name + ' < ' + mlrg[3]
    __set_params(pr, TCm.Blue, line_width, opacity)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[3] + ' - ' + mlrg[3]
    pr.Query  = field_name + ' >= ' + mlrg[3] + ' AND ' + field_name + ' < ' + mlrg[4]
    __set_params(pr, TCm.Green, line_width, opacity)


    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[4] + ' - ' + mlrg[5]
    pr.Query  = field_name + ' >= ' + mlrg[4] + ' AND ' + field_name + ' < ' + mlrg[5]
    __set_params(pr, TCm.Yellow, line_width, opacity)

    li.Add()
    pr = __last(li)
    pr.Legend = mlrg[5] + ' - ' + mlrg[6]
    pr.Query  = field_name + ' >= ' + mlrg[5] + ' AND ' + field_name + ' < ' + mlrg[6]

    __set_params(pr, TCm.Red, line_width, opacity)

    li.Add()
    pr = __last(li)
    pr.Legend = ' >= ' + mlrg[6]
    pr.Query  = field_name + ' >= ' + mlrg[6] + ' AND ' + field_name + ' < ' + mlrg[7]

    __set_params(pr, TCm.Purple, line_width, opacity);


def __set_params(pr, color, line_width, opacity):
    pr.Area.Color = dk_color(color, opacity)
    pr.Area.OutlineWidth = line_width
    pr.Area.OutlineColor = pdk.TGIS_Color.Gray
    pr.Area.ShowLegend = True




def __last(li):
    return li.Items(li.Count - 1)