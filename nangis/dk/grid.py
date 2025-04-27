# 2025-02-12: grid operations
# mareko@hi.no
import tatukgis_pdk as pdk

def export_to_grd(pix : pdk.TGIS_LayerPixel, fname : str, extent : pdk.TGIS_Extent = None) -> None:
    """
     Exports pixel layet to grid file
    :param pix:
    :param fname:
    :return: None
    """
    out = pdk.TGIS_LayerGRD()
    out.Path = fname
    if extent is None:
        extent = pix.Extent
    out.ImportLayer(pix, extent, pix.CS, pix.BitWidth, pix.BitHeight);
