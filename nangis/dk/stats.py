# statistical operations

import tatukgis_pdk as pdk
from nangis.dk.utils import has_fields
qcMISSING_NUMBER = -99999999
def integrate(source: pdk.TGIS_LayerVector,
              fieldNames: list[str],
              units: str,
               missingValue: float = qcMISSING_NUMBER
              ) -> list[float]:
    """
    For source layer containing voronoi polygons
    computes integrals of all fields and their non-zero areas
    returning them as as list of floating point value
    list[0]  - total area of the polygon
    list[1] number of polygons
    list[i] - integral for filed i
    list[i + 1] non-zero area forfiled i
    :param source:
    :param fieldNames:
    :param missingValue:
    :param units: 'km', 'nmi' or
    :return:
    """

    if not has_fields(source, fieldNames):
        raise ValueError('integrate(): some fields from the list are not in the layer')

    Nfields = len(fieldNames)
    Result = [0.0] * (2 + 2 * Nfields)  # total area + count + 2 values per field
    # coefficient because tatukgis uses meters
    if units == 'km':
        multi = 1.0 / (1000.0 * 1000.0)
    else: #elif units == 'nmi':
        multi = 1.0 / (1852.0 * 1852.0)  # square nautical miles
    # else:
    #     multi = 1.0

    k = 0
    for poly in source.Loop():
        if poly is None:
            continue
        if poly.ShapeType != pdk.TGIS_ShapeType().Polygon:
            continue
        area = poly.AreaCS() * multi
        Result[0] += area  # total area

        j = 2
        for i in range(Nfields):
            val = poly.GetField(fieldNames[i]) # must check type
            if val == qcMISSING_NUMBER:
                Result[j] = missingValue
                Result[j + 1] = 0.0
            elif val > 0:
                Result[j] += val * area
                Result[j + 1] += area
            j += 2

        k += 1



    Result[1] = k  # number of polygons
    return Result