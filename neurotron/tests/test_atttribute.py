# test_attribute.py: test attribute module

import doctest
import pytest

import neurotron.math.attribute


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

def test_doctest(validator):
   result = doctest.testmod(neurotron.math.attribute, verbose=False)
   assert result.failed == 0
