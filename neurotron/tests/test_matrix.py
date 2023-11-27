# test_matrix.py: test matrix module

import doctest
import pytest
import neurotron.matrix

#===============================================================================
# fixture
#===============================================================================

@pytest.fixture
def validator():
    return Validator()

class Validator:
    def call(self,func) -> bool:
        return func()

    def validate(self,mode) -> bool:
        if mode == 'good':
            return True
        elif mode == 'exception':
            raise Exception('some exception')
        return False

#===============================================================================
# doctest
#===============================================================================

def test_doctest(validator):
   result = doctest.testmod(neurotron.matrix, verbose=False)
   assert result.failed == 0

#===============================================================================
# using Validator
#===============================================================================

def test_zerodiv(validator):
    with pytest.raises(ZeroDivisionError):
        validator.call(lambda: 5/0)
