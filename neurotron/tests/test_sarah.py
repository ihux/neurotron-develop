# test_sarah.py: test neurotron against `Sarah` sample

import doctest, pytest, sys, os
from neurotron import Token, Toy, Cells, Train, Terminal

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

def test_doctest_me(validator):
    sys.path.append(os.path.dirname(__file__))
    import test_sarah as me

    result = doctest.testmod(me)
    assert result.failed == 0

#===============================================================================
# unit doctest
#===============================================================================

def test_tokenizing():
    """
    # Create a Tokenizer

    >>> token = Token({'Sarah':[1,1,0,1,1,1,0,1,0,1],
    ...            'loves':[0,1,1,1,0,1,1,0,1,1],
    ...            'music':[1,1,1,0,0,1,0,1,1,1],
    ...            '.':    [0,0,0,0,0,0,0,0,0,0]}); token
    Token({
      'Sarah': [1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
      'loves': [0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
      'music': [1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
      '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    })

    # A simpler way would be to consult the Toy class:

    >>> token = Toy('Sarah').token; print(token)
    Token({
      'Sarah': [1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
      'loves': [0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
      'music': [1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
      '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    })
    """

def test_decode():
    """
    >>> # The Token class provides a method for decoding tokens
    >>> token = Toy('Sarah').token;  print(token)
    Token({
      'Sarah': [1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
      'loves': [0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
      'music': [1, 1, 1, 0, 0, 1, 0, 1, 1, 1],
      '.': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    })
    >>> print(token.decode([1,1,0,1,1,1,0,1,0,1]))  # token for 'Sarah'
    Sarah
    >>> print(token.decode([0,1,1,1,0,1,1,0,1,1]))  # token for 'loves'
    loves
    >>> print(token.decode([1,1,1,0,0,1,0,1,1,1]))  # token for 'music'
    music
    """
