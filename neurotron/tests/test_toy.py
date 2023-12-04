# test_toy.py: test neurotron.cluster.toy module

import doctest
import pytest

import neurotron.cluster.toy

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
   result = doctest.testmod(neurotron.cluster.toy)
   assert result.failed == 0
