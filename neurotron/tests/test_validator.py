import pytest
from neurotron.validator import PhoneNumberValidator


VALID_PHONE_NUMBER="+12069220880"
INVALID_PHONE_NUMBER="+15551234"
PHONE_NUMBER_WITHOUT_COUNTRY_CODE="2069220880"


@pytest.fixture
def pn_validator():
    return PhoneNumberValidator(api_key="test_api_key")


def test_valid_phone_number(pn_validator, requests_mock):
    requests_mock.get(pn_validator.api_url + VALID_PHONE_NUMBER, json={"valid": True})
    assert pn_validator.validate(VALID_PHONE_NUMBER) == True


def test_invalid_phone_number(pn_validator, requests_mock):
    requests_mock.get(pn_validator.api_url + INVALID_PHONE_NUMBER, json={"valid": False})
    assert pn_validator.validate(INVALID_PHONE_NUMBER) == False


def test_api_call_failure(pn_validator, requests_mock):
    requests_mock.get(pn_validator.api_url, status_code=500)
    with pytest.raises(Exception):
        pn_validator.validate(INVALID_PHONE_NUMBER)


def test_phone_number_without_country_code(pn_validator, requests_mock):
    requests_mock.get(
        pn_validator.api_url + PHONE_NUMBER_WITHOUT_COUNTRY_CODE, json={"valid": True, "country_code": "US"}
    )
    assert pn_validator.validate(PHONE_NUMBER_WITHOUT_COUNTRY_CODE, country_code="US") == True


def test_phone_number_with_unsupported_country_code(pn_validator, requests_mock):
    requests_mock.get(pn_validator.api_url, status_code=400)
    with pytest.raises(Exception):
        pn_validator.validate(VALID_PHONE_NUMBER, country_code="ZZ")


def test_invalid_api_key(pn_validator, requests_mock):
    requests_mock.get(pn_validator.api_url, status_code=401)
    with pytest.raises(Exception):
        pn_validator.validate(VALID_PHONE_NUMBER)


def test_invalid_phone_number_type(pn_validator):
    with pytest.raises(TypeError):
        pn_validator.validate(5551234)


def test_empty_phone_number(pn_validator):
    with pytest.raises(ValueError):
        pn_validator.validate("")

#===============================================================================
# fixture
#===============================================================================

@pytest.fixture
def validator():
    return Validator()

class Validator:
    def validate(self,mode) -> bool:
        if mode == 'good':
            return True
        elif mode == 'bad':
            return False
        elif mode == 'zerodiv':
            a = 5/0
        return False

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
