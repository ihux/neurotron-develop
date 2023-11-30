# test_attribute.py: test matrix module

import doctest
import pytest

import neurotron.matrix.attribute


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
   result = doctest.testmod(neurotron.matrix.attribute, verbose=False)
   assert result.failed == 0
