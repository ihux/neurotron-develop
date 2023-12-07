"""
test_file.py: doc testing this file
>>> 2+5
7
"""

import doctest, pytest, sys, os

#===============================================================================
# importing me
#===============================================================================

#def thisfile():
#    import sys, os
#    dir = os.path.dirname(__file__)
#    filename = os.path.basename(__file__)
#    file,ext = os.path.splitext(filename)
#    sys.path.append(dir)
#    print('module:',file)
#    return file
#
# file = thisfile()

#def thatfile():
#    import sys, os
#    dir = os.path.dirname(__file__)
#    sys.path.append(dir)

#thatfile()
#import test_file as me

#===============================================================================
# print some stuff
#===============================================================================

#print("testing test_file.py")
#print('__file__:',__file__)
#print('path():',path())

#ok = "well done :-)";

#if __name__ == '__main__':
#    print(me.ok)

#===============================================================================
# fixture
#===============================================================================

@pytest.fixture
def validator():
    return Validator()

class Validator:
    pass

#===============================================================================
# doctest
#===============================================================================

def test_me(validator):
    sys.path.append(os.path.dirname(__file__))
    import test_file as me

    result = doctest.testmod(me)
    assert result.failed == 0
