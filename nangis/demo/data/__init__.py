#
import os
import nangis.demo.data as data

def test_stratum():
    data_dir = os.path.dirname(data.__file__)
    return os.path.join(data_dir, 'edited_stratum.shp')

def test_data():
    data_dir = os.path.dirname(data.__file__)
    return os.path.join(data_dir, 'dummy_nasc.shp')

def test_map():
    data_dir = os.path.dirname(data.__file__)
    return os.path.join(data_dir, 'se_atlatic_coast.shp')
