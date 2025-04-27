# various supportin functions
# 2025-02-04
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


def ndims(ob):
    """
     Returns number of dimensions of an object
    :param ob:
    :return: 0 for non-arrays or non list arrays; otherwise number of relations
    """

    try:
        l = len(ob)
    except:
        return 0
    return len(np.shape(ob))

def is_vec(ob, length=None):
    """
        Checks if an object (list or array) is a vector
        :param ob: an object to test
        :param LENGTH: checks for exact vector size
        :return: True if ob is a 1D vector, False otherwise
        """

    nd = ndims(ob)
    if nd != 1:
        return False
    else:
        if length is None:
            return True
        if np.shape(ob)[0] != length:
            return False
        else:
            return True

def figsize(dx, dy):
    """
        A shortcut for the figure size
        :  param dx: horizontal size in cm
        :param dy: vertical size in cm
        :return: None
    """
    plt.rcParams['figure.figsize'] = (dx, dy)


def str_index(lst, target):
    """
    Returns the index of a list in target string
    :param lst: lsit containing strings
    :param target: string to check
    :return: index of target or -1 if there is no traget
    """
    try:
        return lst.index(target)
    except ValueError:
        return -1

def is_jython():
    """
     Tells the interpreter in use is jython
    """
    return os.name == 'java'

def is_win():
    """
     Checks if the interpreter runs on a
     Windows platform
    """
    if is_jython():
        import java.lang
        return java.lang.System.getProperties()['os.name'][0:4] == 'Wind'
    else:
        return os.name == 'nt'

def is_macosx():
    """
        Checks if the interpreter runs on a
        Windows platform
       """
    if is_jython():
        import java.lang
        return java.lang.System.getProperties()['os.name'] == 'Mac OS X'
    else:
        return sys.platform == 'darwin'

def is_linux():
    """
        Checks if the interpreter runs on a
        Windows platform
       """
    if is_jython():
        import java.lang
        return java.lang.System.getProperties()['os.name'] == 'Linux'
    else:
        return sys.platform.startswith('linux')