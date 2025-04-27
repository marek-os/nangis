# handles comscatter layer access



import tatukgis_pdk as pdk
#from typing import Union
import nangis.dk.db.dkio as SqliteFile


import os

LAYER_COMSCATTER ='LSSS_REPORT'
def load(fileName : str) -> pdk.TGIS_LayerVector:
    """
     Loads comscatter layer from .nclim file
    :param fileName:
    :return:
    """
    if not os.path.isfile(fileName):
        raise FileNotFoundError('nclim file not found')
    return   SqliteFile.open_vector_layer(fileName, LAYER_COMSCATTER);

if __name__ == '__main__':
    from nangis.dk.utils import get_field_names
    from nangis.dk.panda import as_dataframe
    fname = '/media/marek/P2021_02/VOLUME/SARDCLIM/2024-12-08_experiments/NASC/1998409.nclim'
    layer = load(fname)
    fields = get_field_names(layer)
    print('dataaa loaded the fields printed below')
    i = 0
    #[i := i + 1, print(a)] for a in fields]
    [print(f'{i} {a}') for i, a in enumerate(fields, start=1)]
    print(' ---- And now do the pandas dataaa frame')
    df = as_dataframe(layer)
    #print(df.head())
    print(df.iloc[:, :4].head())

