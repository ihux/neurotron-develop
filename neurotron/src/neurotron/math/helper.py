"""
module neurotron.math.helper: helper functions
    _min       minimum of two numbers
    _max       maximum of two numbers
    isa        shorthand for isinstance
    isnumber   is object a number class
"""

import numpy as np

#===============================================================================
# helper
#===============================================================================

isa = isinstance

def isnumber(arg):
    """
    >>> isnumber(5) and isnumber(3.14)
    True
    >>> isnumber(True) and isnumber(False)
    True
    >>> isnumber('abc') or isnumber([])
    False
    """
    if isa(arg,int) or isa(arg,float): return True
    if isa(arg,np.int64) or isa(arg,np.float64): return True
    if isa(arg,bool): return True
    return False

def _max(x,y):
    """
    >>> _max(1,2)
    2
    """
    return x if x > y else y

def _min(x,y):
    """
    >>> _min(1,2)
    1
    """
    return x if x < y else y
