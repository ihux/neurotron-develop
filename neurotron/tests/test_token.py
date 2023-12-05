# test_token.py: test neurotron.cluster.token module

import doctest
import pytest

import neurotron.cluster.token

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
   result = doctest.testmod(neurotron.cluster.token)
   assert result.failed == 0
