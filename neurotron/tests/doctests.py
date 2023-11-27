# tests.py: run all relevant doctests

import doctest
import neurotron.neurotron
import neurotron.matrix
import neurotron.cluster.setup
from neurotron.ansi import Ansi

err = 0
err += doctest.testmod(neurotron.neurotron, verbose=False).failed
err += doctest.testmod(neurotron.cluster.setup, verbose=False).failed
err += doctest.testmod(neurotron.matrix, verbose=False).failed



if err:
   print(Ansi.R+'doctests: total fails:'+Ansi.N,err)
else:
   print(Ansi.G+'all doctests: PASSED'+Ansi.N)
