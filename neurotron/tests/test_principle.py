# test_principle.py: demonstrate test principles

import pytest

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
# using Validator
#===============================================================================

def test_good(validator):
    assert validator.validate('good')

def test_bad(validator):
    assert not validator.validate('bad')

def test_zerodiv1(validator):
    with pytest.raises(ZeroDivisionError):
        validator.validate('zerodiv')

def test_zerodiv2(validator):
    with pytest.raises(ZeroDivisionError):
        validator.call(lambda: 5/0)

def test_exception1(validator):
    with pytest.raises(Exception):
        validator.validate('exception')

def test_exception2(validator):
    def f(): raise Exception(''); return 0
    with pytest.raises(Exception):
        validator.call(f)

def test_typeerror(validator):
    with pytest.raises(TypeError):
        validator.validate('typeerror')

def test_valueerror(validator):
    with pytest.raises(ValueError):
        validator.validate('valueerror')
