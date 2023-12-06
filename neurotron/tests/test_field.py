# test_attribute.py: test field module

import doctest
import pytest

import neurotron.math.field


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
   result = doctest.testmod(neurotron.math.field, verbose=False)
   assert result.failed == 0
