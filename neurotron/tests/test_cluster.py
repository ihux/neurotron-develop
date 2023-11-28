# test_cluster.py: test matrix module

import doctest
import pytest

import neurotron.cluster.setup
import neurotron.cluster.terminal

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

def test_terminal(validator):
   result = doctest.testmod(neurotron.cluster.terminal, verbose=False)
   assert result.failed == 0
