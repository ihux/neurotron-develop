# test_trainer.py: test neurotron.cluster.trainer module

import doctest
import pytest

import neurotron.cluster.trainer

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
   result = doctest.testmod(neurotron.cluster.trainer)
   assert result.failed == 0
