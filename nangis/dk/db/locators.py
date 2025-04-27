# utilities for access
# dk sqlite structures
import sys
def db_layer_locator(file_name: str, layer_name: str) -> str:
    return (
        "[TatukGIS Layer]\n"
        "Storage=Native\n"
        f"LAYER={layer_name.upper()}\n"
        "DIALECT=SQLITE\n"
        f"Sqlite={sys_path_to_sqlite_path(file_name)}\n"
        "ENGINEOPTIONS=16\n"
        ".ttkls"
    )
def grid_layer_locator(file_name: str, layer_name: str) -> str:
    return (
        "[TatukGIS Layer]\n"
        "Storage=Gpkg\n"
        f"LAYER={layer_name}\n"
        "DIALECT=SQLITE\n"
        f"Sqlite={sys_path_to_sqlite_path(file_name)}\n"
        ".ttkps"
    )
def pix_layer_locator(file_name: str, layer_name: str) -> str:
    result = (
        "[TatukGIS Layer]\n"
        "Storage=PixelStore2\n"
        f"LAYER={layer_name}\n"
        "DIALECT=SQLITE\n"
        f"Sqlite={sys_path_to_sqlite_path(file_name)}\n"
        ".ttkps"
    )
    return result

def prepend_slash_n(path: str) -> str:
    result = ''
    remaining = path

    while remaining:
        slash = remaining.find('\\')
        if slash == -1:
            slash = len(remaining)

        processed = remaining[:slash + 1] if slash < len(remaining) else remaining

        if slash < len(remaining) - 1:
            if remaining[slash + 1] == 'n':
                processed += '\\'  # Add an extra backslash to avoid separation

        result += processed
        remaining = remaining[slash + 1:] if slash < len(remaining) else ''

    return result


def sys_path_to_sqlite_path(path: str) -> str:
   # import sys

    # Check if running on Windows
    if sys.platform.startswith('win'):
        if len(path) > 2 and path[1] == ':':
            txtarr = prepend_slash_n(path).split(':')

            if len(txtarr) == 2:
                result = txtarr[0] + ':\\' + txtarr[1]
            else:
                raise RuntimeError(
                    f'PANIC: sys_path_to_sqlite_path: impossible path expression!: {path}'
                )
        else:
            result = path
    else:
        result = path

    return result