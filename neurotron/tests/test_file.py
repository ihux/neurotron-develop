"""
test_file.py: doc testing this file
>>> 2+5
4
"""

import sys, os

def path():
    return os.path.dirname(__file__)
sys.path.append(path())

import test_file

import doctest
import pytest

import neurotron.cluster.setup

#===============================================================================
# print some stuff
#===============================================================================



#print("testing test_file.py")
#print('__file__:',__file__)
#print('path():',path())

ok = "well done :-)";

if __name__ == '__main__':
    print(test_file.ok)

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

def test_setup(validator):
   result = doctest.testmod(neurotron.cluster.setup, verbose=False)
   assert result.failed == 0

def test_self(validator):
   result = doctest.testmod(neurotron.cluster.setup, verbose=False)
   assert result.failed == 0
