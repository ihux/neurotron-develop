# test_matfun.py: test matrix function module

import doctest
import pytest

import neurotron.math.matfun


#===============================================================================
# fixture
#===============================================================================

@pytest.fixture
def validator():
    return Validator()

class Validator:
    def call(self,func) -> bool:
        return func()

#===============================================================================
# doctest
#===============================================================================

def test_doctest(validator):
   result = doctest.testmod(neurotron.math.matfun, verbose=False)
   assert result.failed == 0
