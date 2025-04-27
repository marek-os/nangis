from enum import Enum
import tatukgis_pdk as pdk


class TCm(Enum):
    Aqua        = 0xff00ffff
    Black       = 0xff000000
    Green       = 0xff008000
    DarkGreen  =  0xff006400
    LightGreen  = 0xff90ee90
    DimGray     = 0xff696969
    Fuchsia     = 0xffff00ff
    LightGray   = 0xffd3d3d3 # 0xffd3d3d3 #
    Lime        = 0xff00ff00
    Maroon      = 0xff800000
    Navy        = 0xff000080
    Olive       = 0xff808000
    Purple      = 0xff800080
    Red         = 0xffff0000
    RenderColor = 0x00ff9933
    Silver      = 0xffc0c0c0
    Teal        = 0xff008080
    White       = 0xffffffff
    Yellow      = 0xffffff00
    Gray        = 0xff808080
    Blue        = 0xff0000ff
    Brown       = 0xff964b00
    # Crazy, None can be handled separately if needed

def dk_color(color: TCm, opacity: int) -> pdk.TGIS_Color:
    col = color.value if isinstance(color, TCm) else 0xff808080

    # Calculate alpha (opacity in % to 0–255 scale)
    opa = (opacity * 255) // 100
    opa = opa << 24

    # Strip existing alpha, apply new one
    col = (col & 0x00ffffff) | opa
    return pdk.TGIS_Color.FromARGB(col)

# class TCm(Enum):
#     Aqua        = 0xff00ffff
#     Black       = 0xff000000
#     Green       = 0xff008000
#     DimGray     = 0xff696969
#     Fuchsia     = 0xffff00ff
#     LightGray   = 0xffd3d3d3
#     Lime        = 0xff00ff00
#     Maroon      = 0xff800000
#     Navy        = 0xff000080
#     Olive       = 0xff808000
#     Purple      = 0xff800080
#     Red         = 0xffff0000
#     RenderColor = 0x00ff9933
#     Silver      = 0xffc0c0c0
#     Teal        = 0xff008080
#     White       = 0xffffffff
#     Yellow      = 0xffffff00
#     Gray        = 0xff808080
#     Blue        = 0xff0000ff
#
# def dk_color(color: TCm, opacity: int) -> pdk.TGIS_Color:
#     col = color.value  # direct ARGB from the enum
#     opa = int((opacity * 255) / 100) << 24
#     col = (col & 0x00ffffff) | opa
#     return pdk.TGIS_Color.FromARGB(col)