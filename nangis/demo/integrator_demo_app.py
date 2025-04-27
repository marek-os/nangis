# Created by mareko@hi.no at 03.03.2025

import tatukgis_pdk as pdk
from nangis.os_utils import is_linux, is_macosx

import nangis.demo.data as data
from nangis.demo.dk_helpers import build_rectangular_voronoi, integrate_nansen_region, build_voronoi_over_stratum

#from nangis.dk.utils import get_shape
import numpy as np
import os
import nangis.dk as dk


LAYER_RECT_VORONOI='RECTANGULAR VORONOI'
LAYER_MASTER_STRATUM = 'MASTER_STRATUM'
LAYER_VORONOI_OVER_STRATUM = 'VORONOI_OVER_STRATUM'

class FormIntegratorSensivityTest(pdk.TGIS_PvlForm):



    def __init__(self, _owner):
        self._bCreated = False
        self.Caption = "Fish length Histogram - NANGIS test"
        if is_linux():
            cwith = 600*3
            cheight = 430*3
        else:
            cwith = 700*2
            cheight = 530*2
        self.ClientWidth = cwith
        self.ClientHeight = cheight

        self.OnShow = self.form_show

        self.__init_toolbar()
        self.__init_boilerPlate()
        self.__init_actionProgress()
        self.__init_actionPane()
        self.__init_control_panel_left()
        self.__init_gis_panel()

        self.GIS = pdk.TGIS_ViewerWnd(self.gisPanel.Context)
        self.GIS_legend.GIS_Viewer = self.GIS
        self.GIS_legend.Mode = pdk.TGIS_ControlLegendMode().Layers

        #self.GIS.Align = "Client"

        self.GIS.Left = 152
        self.GIS.Top = 12
        self.GIS.Width = 420*3
        self.GIS.Height = 358*3
        self.GIS.Anchors = (pdk.TGIS_PvlAnchor().Left, pdk.TGIS_PvlAnchor().Top,
                           pdk.TGIS_PvlAnchor().Right, pdk.TGIS_PvlAnchor().Bottom)

        self.GIS.Graticule.HorizontalStyle.Step = - 4.0
        self.GIS.Graticule.VerticalStyle.Step = - 4.0
        self.GIS.Graticule.Enabled = True

        self.bispecies = None
        self.comscatter = None
        self.GIS.Align = "Client"

    def form_show(self, _sender):
        if self._bCreated:
            return


        lmap = dk.load_shp(data.test_map(), 'LAYER_MAP')
        lmap.SetCSByEPSG(4326)
        ldata = dk.load_shp(data.test_data(), 'LAYER_DATA')
        ldata.SetCSByEPSG(4326)
        dk.set_style_nansen_report(ldata, 'FISH_SA')
        lstratum = dk.load_shp(data.test_stratum(), 'STRATUM1')
        lstratum.SetCSByEPSG(4326)
        lstratum.Name = LAYER_MASTER_STRATUM
        dk.set_stratum_yellow_semitransparent(lstratum)

        lvor = build_rectangular_voronoi(ldata, lstratum, lmap)
        lvor.Name = LAYER_RECT_VORONOI
        dk.set_style_nansen_voronoi_map(lvor, 'FISH_SA')

        lvor2 = build_voronoi_over_stratum(ldata, lstratum)
        lvor2.Name = LAYER_VORONOI_OVER_STRATUM
        dk.set_style_nansen_voronoi_map(lvor2, 'FISH_SA')

         # clip voronoi to a layer
        #lvor_clip = copy_clipped_layer(lvor, get_shape(lstratum, 0))
        #set_style_nansen_voronoi_map(lvor_clip, 'FISH_SA')

        # buf = build_shape_buffer(get_shape(lstratum, 0), -1.0 * 0.008999928)
        # lvor_clip = copy_clipped_layer(lvor, buf)
        # set_style_nansen_voronoi_map(lvor_clip, 'FISH_SA')

        # for shp in ldata.Loop():
        #     print(shp.getField('FISH_SA'))

        self.GIS.Lock()

        self.GIS.Add(lvor2)
        self.GIS.Add(lmap)

        self.GIS.Add(ldata)
        self.GIS.Add(lstratum)

        self.GIS.SetCSByEPSG(4326)
       # self.GIS.Graticule().Enabled(True)

        #self.GIS.FullExtent()
        self.GIS.VisibleExtent = lstratum.Extent
        self.GIS.InvalidateWholeMap()
        self.GIS.Unlock()

        self._bCreated = True

    def __init_gis_panel(self):
        """
        Panle holding gis and lagend
        :return: None
        """
        self.gisPanel = pdk.TGIS_PvlPanel(self.actionPane.Context)
        self.gisPanel.Align = "Client"
        self.GIS_legend = pdk.TGIS_PvlControlLegend(self.gisPanel.Context)
        self.GIS_legend.Align = "Right"
        self.GIS_legend.Width = 300
        self.GIS_legend.DrawIconStyle = pdk.TGIS_LegendIconStyle().Rectangular

    def __init_toolbar(self):
        """
        initialises top toolbar
        """
        self.toolbar_buttons = pdk.TGIS_PvlPanel(self.Context)
        self.toolbar_buttons.Place(592, 29, None, 0, None, 0)
        self.toolbar_buttons.Align = "Top"

        self.button1 = pdk.TGIS_PvlButton(self.toolbar_buttons.Context)
        self.button1.Place(75, 22, None, 3, None, 3)
        self.button1.Caption = "Full Extent"
        self.button1.OnClick = self.btnFullExtent_click

        self.button2 = pdk.TGIS_PvlButton(self.toolbar_buttons.Context)
        self.button2.Place(75, 22, None, 79, None, 3)
        self.button2.Caption = "Zoom"
        self.button2.OnClick = self.btnZoom_click

        self.button3 = pdk.TGIS_PvlButton(self.toolbar_buttons.Context)
        self.button3.Place(75, 22, None, 156, None, 3)
        self.button3.Caption = "Drag"
        self.button3.OnClick = self.btnDrag_click

        self.CmbColums = pdk.TGIS_PvlComboBox(self.toolbar_buttons.Context)
        self.CmbColums.Place(175, 22, None, 300, None, 3)
        # names = ("Normal.ttkproject",
        #          "Normal with histogram.ttkproject",
        #          "Grayscale.ttkproject",
        #          "Colorize.ttkproject",
        #          "Inversion.ttkproject",
        #          "Inversion by RGB.ttkproject")
        # for name in names:
        #     self.ComboProject.ItemsAdd(name)
        self.CmbColums.OnChange = self.OnColumnChange

        # -- end form pixel
    def __init_boilerPlate(self):
          # create boilerplate panel (whole form area except toolbar)
        self.boilerPlate =  pdk.TGIS_PvlPanel(self.Context)
        self.boilerPlate.Align = "Client"

    def __init_actionPane(self):
        # action pane - clinet of the boilerplate -
        # progress bar in the bottom
         self.actionPane  =  pdk.TGIS_PvlPanel(self.boilerPlate.Context)
         self.actionPane.Align = "Client"

    def __init_actionProgress(self):
         self.progressBar1 = pdk.TGIS_PvlLabel(self.boilerPlate.Context)
         self.progressBar1.Align = "Bottom"
         self.progressBar1.Height = 50

        # self.progressBar1.Place(142, 23, None, 192, None, 376)
        # self.progressBar1.Anchors = (pdk.TGIS_PvlAnchor().Left, pdk.TGIS_PvlAnchor().Right, pdk.TGIS_PvlAnchor().Bottom)
         self.progressBar1.Visible = False

    def __init_control_panel_left(self):
         # create panel for interpolation controls
        self.leftPanel =  pdk.TGIS_PvlPanel(self.actionPane.Context)
        self.leftPanel.Width = 200
        self.leftPanel.Align = "Left"
        pself = self.leftPanel
        offs = 13

        self.btnGenerate = pdk.TGIS_PvlButton(pself.Context)
        self.btnGenerate.Place(134, 23, None, 12, None, offs + 13) #+ 100 - 13)  #376)
        #self.btnGenerate.Anchors = (pdk.TGIS_PvlAnchor().Left, pdk.TGIS_PvlAnchor().Bottom)
        self.btnGenerate.Caption = "Sensitivity test"
        self.btnGenerate.OnClick = self.OnBtnGenerateFired

    # def rbAny_change(self, _sender):
    #     if self.rbKriging.Checked:
    #         self.lblSemivariance.Visible = True
    #         self.cbSemivariance.Visible = True
    #     else:
    #         self.lblSemivariance.Visible = False
    #         self.cbSemivariance.Visible = False

    def doBusyEvent(self, _sender, pos, _end, _abort):
        pass

    # def doIDW(self):
    #     pass
    #
    # def doKriging(self):
    #     pass
    # def doSplines(self):
    #     pass
    #
    # def doHeatmap(self, concentration):
    #     pass
    #
    def OnBtnGenerateFired(self, _sender):
       lvor = self.GIS.get(LAYER_RECT_VORONOI)
       lstratum = self.GIS.get(LAYER_MASTER_STRATUM)
       print('--- computing, please wait --')
       no, ce, so = integrate_nansen_region(lvor, dk.get_shape(lstratum, 0), -2.0, 2.0, 0.1)
       self.describe(no[:, 2], 'Norhern region')
       self.describe(ce[:, 2], 'Central region')
       self.describe(so[:, 2], 'Southern region')

    def describe(self, column, name):
        me = np.mean(column)
        st =  np.std(column)
        print(f"\nStatistics for {name}:")
        print("Mean:      ", me)
        print("Std dev:   ", st)
        print("Std/mean %:", st/me * 100)
        print("Median:    ", np.median(column))
        print("25th pct:  ", np.percentile(column, 25))
        print("75th pct:  ", np.percentile(column, 75))
    def btnFullExtent_click(self, _sender):
        if self.GIS.IsEmpty:
            return
        self.GIS.FullExtent()

    def btnZoom_click(self, _sender):
        if self.GIS.IsEmpty:
            return
        print('Zoom clicked')
        self.GIS.Mode = pdk.TGIS_ViewerMode().Zoom

    def btnDrag_click(self, _sender):
        if self.GIS.IsEmpty:
            return
        self.GIS.Mode = pdk.TGIS_ViewerMode().Drag

    def OnColumnChange(self, _sender):
        pass
        #project = self.ComboProject.Text
        #self.GIS.Open(pdk.TGIS_Utils.GisSamplesDataDirDownload() +
        #              "Samples/Projects/" + project)

    def _activeColumn(self):
        # column currently selected in combo
        return self.CmbColums.Item(self.CmbColums.ItemIndex)


def main():
    frm = FormIntegratorSensivityTest(None)
    frm.Show()
    pdk.RunPvl(frm)

if __name__ == '__main__':
    main()
