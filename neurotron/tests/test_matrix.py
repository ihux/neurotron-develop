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

def doctests(module):
    return doctest.testmod(module, verbose=False).failed == 0

class Validator:
    def validate(self,mode) -> bool:
        if mode == 'good':
            return True
        elif mode == 'bad':
            return False
        elif mode == 'zerodiv':
            a = 5/0
        elif mode == 'exception':
            raise Exception('some exception')
        elif mode == 'typeerror':
            raise TypeError('bad type')
        elif mode == 'valueerror':
            raise ValueError('bad value')
        return False

#===============================================================================
# doctest
#===============================================================================

def test_doctest(validator):
   assert doctests(neurotron.matrix)

#===============================================================================
# using Validator
#===============================================================================

def test_good(validator):
    assert validator.validate('good')

def test_bad(validator):
    assert not validator.validate('bad')

def test_zerodiv(validator):
    with pytest.raises(ZeroDivisionError):
        validator.validate('zerodiv')

def test_exception(validator):
    with pytest.raises(Exception):
        validator.validate('exception')

def test_typeerror(validator):
    with pytest.raises(TypeError):
        validator.validate('typeerror')

def test_valueerror(validator):
    with pytest.raises(ValueError):
        validator.validate('valueerror')
