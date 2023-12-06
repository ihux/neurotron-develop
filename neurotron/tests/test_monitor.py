# test_attribute.py: test attribute module

import doctest
import pytest

import neurotron.cluster.monitor

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
   result = doctest.testmod(neurotron.cluster.monitor)
   assert result.failed == 0
