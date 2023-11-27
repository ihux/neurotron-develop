# tests.py: run all relevant doctests

import doctest
import neurotron.neurotron
import neurotron.matrix

#doctest.testmod(neurotron.neurotron, verbose=True)
doctest.testmod(neurotron.matrix, verbose=False)
