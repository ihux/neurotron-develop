# test_cluster.py: test matrix module

import doctest
import pytest

import neurotron.cluster.setup

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
   result = doctest.testmod(neurotron.cluster.setup, verbose=False)
   assert result.failed == 0
