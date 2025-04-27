# sqlite retated operations

#from tatukgis_pdk import TGIS_LayerSqlSqlite, TGIS_LayerPixelStoreSqlite, TGIS_LayerPixel
import tatukgis_pdk  as pdk
from nangis.dk.utils import has_any_shapes
from nangis.dk.db.locators import db_layer_locator, pix_layer_locator

def open_layer_vector2(file_name: str, vl_template) -> pdk.TGIS_LayerSqlSqlite:
    lsql = pdk.TGIS_LayerSqlSqlite()
    lsql.path = db_layer_locator(file_name, vl_template.name)
    lsql.open()
    lsql.caption = vl_template.caption
    lsql.name = vl_template.name
    lsql.params.line.color = vl_template.params.line.color

    if not has_any_shapes(lsql):
        # No need to call lsql.free() in Python
        return None

    return lsql

def open_layer_vector(file_name: str, layer_name: str) -> pdk.TGIS_LayerVector:
    """
     @deprecated(reason="Use `open_layer_sql()` instead.")
     Opens vector layer from database and cast it general vector layer
    :param file_name:
    :param layer_name:
    :return: TGIS_LayerVectorType
    """
    # lsql = pdk.TGIS_LayerSqlSqlite()
    # lsql.path = db_layer_locator(file_name, layer_name)
    # #print(lsql.path)
    # lsql.open()
    #
    # if not has_any_shapes(lsql):
    #     # No need for manual memory management in Python
    #     print('*** I did not find any shapes here')
    #     return None

    #return lsql
    return open_layer_sql(file_name, layer_name)

def open_layer_sql(file_name: str, layer_name: str) -> pdk.TGIS_LayerSqlSqlite:
    """
     Opens SolSqlite layer from sql database
    :param file_name:
    :param layer_name:
    :return:
    """
    lsql = pdk.TGIS_LayerSqlSqlite()
    lsql.path = db_layer_locator(file_name, layer_name)
    #print(lsql.path)
    lsql.open()
    lsql.Name = layer_name
    if not has_any_shapes(lsql):
        # No need for manual memory management in Python
        print('*** I did not find any shapes here')
        return None

    return lsql



def open_pixel_layer(file_name: str, layer_name: str) -> pdk.TGIS_LayerPixel:
    # Create the SQLite pixel store layer
    lsql = pdk.TGIS_LayerPixelStoreSqlite()

    try:
        # Set the path using the pixel layer locator
        lsql.path = pix_layer_locator(file_name, layer_name)
        print(f'> pixel locator: {lsql.path}')
        # Open the layer
        lsql.Name = layer_name
        lsql.open()

        # Return the opened layer
        return lsql

    except Exception as e:
        # Free resources in case of an error

        return None

def store_layer_vector(vec: pdk.TGIS_LayerVector, file_name: str) -> bool:
    """
    Stores a TatukGIS TGIS_LayerVector into an SQLite database.

    Args:
        vec (pdk.TGIS_LayerVector): The source vector layer.
        file_name (str): The SQLite database file path.

    Returns:
        bool: True if storage was successful, False otherwise.
    """
    if vec is None:
        raise ValueError("[store_layer_vector] Source layer cannot be None!")

    lsql = pdk.TGIS_LayerSqlSqlite()
    try:
        lsql.SetCSByEPSG(vec.CS.EPSG)  # Set coordinate system
        lsql.Extent = vec.Extent  # Set extent

        # Generate SQLite storage path
        lsql.Path = db_layer_locator(file_name, vec.Name)

        # Import vector layer into SQLite
        lsql.ImportLayer(vec, vec.Extent, pdk.TGIS_ShapeType().Unknown, "", False)

        # lsql.RecalcExtent()  # Uncomment if needed

        return True  # Success
    except Exception as e:
        print(f"Error storing vector layer: {e}")  # Handle exception
        return False
    finally:
        lsql.Free()  # Ensure memory is freed

if __name__ == '__main__':
    from nangis.dk.basemap.map_layer_names import LAYER_COASTLINE

    FMAP='/Applications/NCLIM/gis/maps/v1/SouthEast_Tropical_Atlantic.abm'
    lay = open_layer_vector(FMAP, LAYER_COASTLINE)
    if lay is None:
        print('Failed to read your layer')
    else:
        print('Success: your layer has been read')
