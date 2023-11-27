# tests.py: run all relevant doctests

import doctest
import neurotron.neurotron
import neurotron.matrix
import neurotron.cluster.setup

#doctest.testmod(neurotron.neurotron, verbose=True)
doctest.testmod(neurotron.matrix, verbose=False)
doctest.testmod(neurotron.cluster.setup, verbose=False)
